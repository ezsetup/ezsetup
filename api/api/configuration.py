import json
from flask import jsonify, request

from api import permission_required
from auth.decorators import login_required

from flask_classful import FlaskView

class Configurations(FlaskView):
    decorators = [login_required, permission_required]

    def index(self):
        """GET /api/configurations/?type= : Return all visible (non hidden) configurations
        File cloudops/configurations/templates.json store a list of available configurations:
            - hidden: implicit configurations, which are not showned to user interface
            - instanceOnly: configurations which are available only for 'normal' instance
        """
        instance_configurations = []
        router_configurations = []

        with open('cloudops/configurations/templates.json') as f:
            templates = json.load(f)
            for template in templates:
                if template.get('hidden', False) is False:
                    instance_configurations.append(template['name'])
                    if template.get('instanceOnly', False) is not True:
                        router_configurations.append(template['name'])
    
        instance_type = request.args.get('type')
        if instance_type == 'instance':
            return jsonify(instance_configurations)
        elif instance_type == 'router':
            return jsonify(router_configurations)
        else:
            return jsonify(message='Bad request: wrong instance type'), 400


