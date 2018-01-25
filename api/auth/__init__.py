from flask import Blueprint
from auth.views import post_user, delete_user, post_token, delete_token

''' Version: 0.17.05.0'''

auth_blueprint = Blueprint('auth', __name__)

"""DEPRECATED
auth_blueprint.add_url_rule(
    '/users/', view_func=post_user, methods=['POST']
)"""

auth_blueprint.add_url_rule(
    '/users/<int:user_id>', view_func=delete_user, methods=['DELETE'])
auth_blueprint.add_url_rule(
    '/tokens/', view_func=post_token, methods=['POST'])
auth_blueprint.add_url_rule(
    '/tokens/', view_func=delete_token, methods=['DELETE'])
