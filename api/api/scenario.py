from flask_classful import FlaskView
from flask import request, jsonify, g, abort, make_response

from models import Scenario
from api import permission_required
from auth.decorators import login_required
from postgrespy import UniqueViolatedError


def _get_scenarios_private_only():
    ret = []
    for scenario in Scenario.fetchall(owner_id=g.user['id']):
        ret.append({
            'id': scenario.id,
            'name': scenario.name,
            'description': scenario.description
        })
    return jsonify(ret)


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

            return jsonify(ret)
