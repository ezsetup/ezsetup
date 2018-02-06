from flask import jsonify, g
from flask_classful import FlaskView

from auth.decorators import login_required
from models import Slice, Instance, Router, NetworkNode, Lab
from api import permission_required
from postgrespy.queries import Select, Join


class Slices(FlaskView):
    decorators = [login_required, permission_required]

    def get(self, id):
        sl = Slice.fetchone(id=id)

        # only user or the lab creator can access
        if sl.user_id != g.user['id']:
            lab = Lab.fetchone(id=sl.lab_id)
            if lab.owner_id != g.user['id']:
                return jsonify(message="Access denied to this slice resource"), 403

        # get networks
        with Select(NetworkNode, 'slice_id=%s and status!=%s') as select:
            select.execute((sl.id, 'inactive'))
            networks = [{
                'id': n.id,
                'name': n.name,
                'cidr': n.cidr,
                'status': n.status,
                'x': n.x,
                'y': n.y,
                'type': 'NetworkNode'
            } for n in select.fetchall()]

        instances = []
        links = []

        # get instances
        with Select(Instance, 'instances.slice_id=%s and instances.status!=%s') as select:
            select.execute((sl.id, 'inactive'))
            results = select.fetchall()
            for res in results:
                instance = res
                instances.append({
                    'id': instance.id,
                    'name': instance.name,
                    'public_ip': instance.public_ip,
                    'status': instance.status,
                    'password': instance.password,
                    'x': instance.x,
                    'y': instance.y,
                    'configurations': instance.configurations.value, # TODO: remove .value here after implement it in postgrespy
                    'type': 'Instance'
                })

                for link in instance.links:
                    links.append({
                        'gid': link['gid'],
                        'ip': link['ip'],
                        'network': link['network'],
                        'target': link['target'],
                        'type': 'NetworkLink'
                    }) 

        # get routers
        routers = []
        with Select(Router, 'routers.slice_id=%s and routers.status!=%s') as select:
            select.execute((sl.id, 'inactive'))
            results = select.fetchall()
            for res in results:
                router = res
                routers.append({
                    'id': router.id,
                    'name': router.name,
                    'public_ip': router.public_ip,
                    'status': router.status,
                    'password': router.password,
                    'x': router.x,
                    'y': router.y,
                    'configurations': router.configurations.value, # TODO: remove .value here after implement it in postgrespy
                    'type': 'Router'
                })

                for link in router.links:
                    links.append({
                        'gid': link['gid'],
                        'ip': link['ip'],
                        'network': link['network'],
                        'target': link['target'],
                        'type': 'NetworkLink'
                    }) 
        return jsonify({
            'status': sl.status,
            'name': sl.name,
            'networks': networks,
            'instances': instances,
            'routers': routers,
            'links': links
        })

    def index(self):
        """ List ONLY slices that a user has been added to"""
        with Select(Slice, 'user_id = %s') as select:
            select.execute((g.user['id'],))
            slices = select.fetchall()
        ret = []
        for sl in slices:
            lab = Lab.fetchone(id=sl.lab_id)
            ret.append({
                'id': sl.id,
                'labName': lab.name
            })
        return jsonify(sorted(ret, key=lambda i: i['id'], reverse=True))
