from functools import wraps
from flask import g, abort, make_response, jsonify, request
import json
from redisdb import redis_token_db
from helpers import get_user_info


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(g, 'user') or g.user is None:
            token = request.headers['Authorization']
            email = request.headers['Email']
            valueStr = redis_token_db.get(email)
            if valueStr is None:
                abort(make_response(
                    jsonify(message="Unauthenticated request: no email"), 401))
            value = json.loads(valueStr)
            if token != value['token']:
                abort(make_response(
                    jsonify(message="Unauthenticated request: wrong password"), 401))
            else:
                g.user = value

                # This is an additional, application-specific step. You can
                # remove it in your application
                get_user_info()

        return f(*args, **kwargs)
    return decorated_function
