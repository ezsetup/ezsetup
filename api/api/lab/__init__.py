from flask import request, jsonify, g
from flask_classful import FlaskView, route

from models import Lab, Slice
from auth.models import User
from api import permission_required
from auth.decorators import login_required

from api.lab.deploy import DeployThread
from api.lab.destroy import DestroyThread

class Labs(FlaskView):
    decorators = [login_required, permission_required]

    def post(self):
        name = request.get_json()['name']
        description = request.get_json()['description']
        scenario_id = request.get_json()['scenarioId']
        new_lab = Lab.insert(name=name, description=description, scenario_id=scenario_id,
                      owner_id=g.user['id'], status='inactive')
        return jsonify(id=new_lab.id)

    def index(self):
        """Get labs as a owner"""
        labs = Lab.fetchall(owner_id=g.user['id'])
        ret = []
        for l in labs:
            ret.append({
                'id': l.id,
                'name': l.name,
                'description': l.description,
                'status': l.status,
                'slices': len(Slice.fetchall(lab_id=l.id))
            })
        return jsonify(sorted(ret, key=lambda i: i['id'], reverse=True))

    def get(self, id):
        lab = Lab.fetchone(id=id)
        if lab is None:
            return jsonify(message="Lab doesn't existed"), 410
        if lab.status == 'inactive':
            return jsonify({
                'id': lab.id,
                'name': lab.name,
                'status': lab.status
            })
        else:
            slices = []
            for sl in Slice.fetchall(lab_id=lab.id):
                user = User.fetchone(id=sl.user_id)
                slices.append({
                    'id': sl.id,
                    'name': sl.name,
                    'status': sl.status,
                    'username': user.fullname
                })
            return jsonify({
                'id': lab.id,
                'name': lab.name,
                'status': lab.status,
                'slices': slices
            })

    @route('/<int:id>/deploy', methods=['POST'])
    def deploy(self, id):
        cloudconfig_id = request.get_json()['cloudConfigId']
        users = request.get_json()['users']
        t = DeployThread(id, cloudconfig_id, users)
        t.start()
        return jsonify(message="ok")

    @route('/<int:id>/destroy', methods=['POST'])
    def destroy(self, id):
        t = DestroyThread(id)
        t.start()
        return jsonify(message="ok")
