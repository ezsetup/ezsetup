from flask_classful import FlaskView
from flask import request, jsonify

from api import permission_required
from auth.decorators import login_required
from models import CloudConfig

from cloudops import CloudOps


class Cloudconfigs(FlaskView):
    decorators = [login_required, permission_required]

    def post(self):
        """Return {id: cloudconfig_id}"""
        provider = request.get_json()['provider']
        detail = request.get_json()['cloudDetail']
        lab_id = request.get_json()['labId']

        # Check if there is an existed cloudconfig for the lab
        cloudconfig = CloudConfig.fetchone(lab_id=lab_id)
        if cloudconfig is not None:
            return jsonify(id=cloudconfig.id)

        # Test connection
        cloudops = CloudOps(provider, detail)
        if cloudops.test_connection():
            """ Only save correct credentials"""
            new_cloudconfig = CloudConfig(
                detail=detail, provider=provider, lab_id=lab_id)
            new_cloudconfig.save()

            return jsonify(id=new_cloudconfig.id)
        else:
            return jsonify(message="Wrong {0} credentials".format(provider)), 412
