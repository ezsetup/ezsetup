from typing import Tuple, List
import ipaddress

from flask_classful import FlaskView
from flask import request, jsonify, g, abort, make_response

from models import Scenario
from . import permission_required
from auth.decorators import login_required
from postgrespy import UniqueViolatedError


def _get_scenarios_private_only():
    ret = []
    for scenario in Scenario.fetchall(owner_id=g.user['id']):
        ret.append({
            'id': scenario.id,
            'name': scenario.name,
            'description': scenario.description,
            'sgRules': scenario.sg_rules,
            'topo': scenario.topo.value
        })
    return jsonify(sorted(ret, key=lambda i: i['id'], reverse=True))


def validate_network(network_config: dict) -> Tuple[bool, List[str]] :
    """ Check if a network configuration is validated
    Return (False, error_messages) if it's not""" 
    valid = True
    error_messages = []

    if not 'name' in network_config or len(network_config['name']) == 0:
        valid = False
        error_messages.append("Network: name required")

    if network_config.get('cidr') is None:
        valid = False
        error_messages.append("Network {0}: cidr required".format(network_config.get('name')))
    else:
        try:
            ipaddress.IPv4Network(network_config['cidr'])
        except ValueError as err:
            valid = False
            error_messages.append("Network {0}: {1}".format(
                network_config.get('name'), str(err)))

    return valid, error_messages

def validate_instance(instance_config: dict) -> Tuple[bool, List[str]] :
    """ Check if an instance configuration is validated
    Return (False, error_messages) if it's not""" 
    valid = True
    error_messages = []

    if instance_config.get('flavor') is None:
        valid = False
        error_messages.append("Instance {0}: flavor required".format(instance_config['name']))

    if instance_config.get('image') is None:
        valid = False
        error_messages.append("Instance {0}: image required".format(instance_config['name']))

    if instance_config.get('name') is None:
        valid = False
        error_messages.append("Instance: name required")

    return valid, error_messages

def validate_router(router_config: dict) -> Tuple[bool, List[str]] :
    """ Check if an instance configuration is validated
    Return (False, error_messages) if it's not""" 
    valid = True
    error_messages = []

    if router_config.get('flavor') is None:
        valid = False
        error_messages.append("Router {0}: flavor required".format(router_config['name']))

    if router_config.get('image') is None:
        valid = False
        error_messages.append("Router {0}: image required".format(router_config['name']))

    if router_config.get('name') is None:
        valid = False
        error_messages.append("Router: name required")

    return valid, error_messages

def validate_links(topo: dict) -> Tuple[bool, List[str]] :
    """ Check if a link configuration is validated
    Return (False, error_messages) if it's not""" 
    valid = True
    error_messages = []

    for link in topo['links']:
        """ Check if the link's target is valid and exists"""
        if link.get('target') is None:
            valid = False
            error_messages.append("Link {0}: target required".format(link['name']))
        else:
            targets :list = []
            if topo.get('instances'):
                targets.extend(topo['instances'])
            if topo.get('routers'):
                targets.extend(topo['routers'])

            target = next(filter(lambda t: t['gid'] == link['target']['gid'], targets), None)
            if target is None:
                valid = False
                error_messages.append(
                    "Link {0}: No such target that has gid {1}".format(
                        link.get('name'),
                        link['target']['gid'])
                )

        """ Check if the link's network is valid and exists"""
        if link.get('network') is None:
            valid = False
            error_messages.append("Link {0}: network required".format(link.get('name')))
        else:
            network = next(filter(lambda n: n['gid'] == link['network']['gid'], topo['networks']), None)
            if network is None:
                valid = False
                error_messages.append(
                    "Link {0}: No such network that has gid {1}".format(
                        link.get('name'),
                        link['network']['gid'])
                )

        """Check if link's ip is in the range of its network cidr"""
        try:
            ip = ipaddress.IPv4Address(link['ip'])
            if link.get('network') is not None: 
                network = next(
                    filter(
                        lambda n: n['gid'] == link['network']['gid'],
                        topo['networks']
                    ), None
                )

                if network:
                    cidr = ipaddress.ip_network(network['cidr'])
                    if ip not in cidr.hosts():
                        valid = False
                        error_messages.append(
                            "Link {0}: ip address {1} is not in cidr {2}".format(
                                link.get('name'),
                                link['ip'],
                                network['cidr']
                            )
                        )

        except ValueError as err:
            valid = False
            error_messages.append("Link {0}: {1}".format(link.get('name'), str(err)))

    return valid, error_messages

def validate_topo(topo: dict) -> Tuple[bool, List[str]]:
    """ Check if a scenario's topo is validated
    Return (False, error_messages) if it's not validated""" 
    valid = True
    error_messages = []

    # validate networks
    if 'networks' in topo:
        for network in topo['networks']:
            v, errs = validate_network(network)
            valid = valid and v
            error_messages.extend(errs)

    # validate instances
    if 'instances' in topo:
        for instance in topo['instances']:
            v, errs = validate_instance(instance)
            valid = valid and v
            error_messages.extend(errs)

    # validate routers
    if 'routers' in topo:
        for router in topo['routers']:
            v, errs = validate_router(router)
            valid = valid and v
            error_messages.extend(errs)

    # validate links
    if 'links' in topo:
        v, errs = validate_links(topo)
        valid = valid and v
        error_messages.extend(errs)

    return valid, error_messages


class Scenarios(FlaskView):
    decorators = [login_required, permission_required]

    def get(self, id):
        scenario = Scenario.fetchone(id=id)
        if scenario is not None:
            return jsonify(id=scenario.id, name=scenario.name,
                           description=scenario.description, sgRules=scenario.sg_rules, topo=scenario.topo.value,
                           isPublic=scenario.is_public.value)
        else:
            return jsonify(message="scenario not found"), 404

    def post(self):
        name = request.get_json()['name']
        description = request.get_json()['description']

        topo = request.get_json()['topo']
        valid, errs = validate_topo(topo)
        if not valid:
            return jsonify(errors=errs), 400

        isPublic = request.get_json()['isPublic']
        sgRules = request.get_json()['sgRules']
        new_scenario = Scenario(owner_id=g.user['id'],
                                name=name, description=description, topo=topo, is_public=isPublic, sg_rules=sgRules)
        try:
            new_scenario.save()
        except UniqueViolatedError:
            abort(make_response(jsonify(message="Duplicated scenario name"), 409))
        return jsonify(id=new_scenario.id)

    def patch(self, id):
        scenario = Scenario.fetchone(id=id)
        if scenario.owner_id != g.user['id']:
            return jsonify(message="You are not the owner of this scenario"), 405

        name = request.get_json()['name']
        description = request.get_json()['description']

        topo = request.get_json()['topo']
        valid, errs = validate_topo(topo)
        if not valid:
            return jsonify(errors=errs), 400
        
        isPublic = request.get_json()['isPublic']
        sgRules = request.get_json()['sgRules']
        scenario.name = name
        scenario.description = description
        scenario.topo = topo
        scenario.is_public = isPublic
        scenario.sg_rules = sgRules
        scenario.save()
        return jsonify(id=id)

    def index(self):
        if request.args.get('privateOnly', 'false') == 'true':
            return _get_scenarios_private_only()
        else:
            public_scenarios = Scenario.fetchall(is_public=True)
            private_scenarios = Scenario.fetchall(
                is_public=False, owner_id=g.user['id'])
            ret = []
            for s in public_scenarios + private_scenarios:
                r = {
                    'id': s.id,
                    'name': s.name,
                    'description': s.description,
                    'sgRules': s.sg_rules,
                    'topo': s.topo.value
                }
                ret.append(r)

            return jsonify(sorted(ret, key=lambda i: i['id'], reverse=True))

    def delete(self, id):
        scenario = Scenario.fetchone(id=id)
        scenario.delete()
        return jsonify(message="ok")
