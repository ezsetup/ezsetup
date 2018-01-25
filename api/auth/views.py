from flask import request, jsonify, g
import secrets
import json
from passlib.hash import argon2

from auth.models import User
from auth.decorators import login_required

from postgrespy import UniqueViolatedError
from redisdb import redis_token_db

# TODO: consider set this value, both in client's Login.vue/Signup.vue and here
# to a longer interval.
# Currently, I set it just one day to have a better chance
# to observe any possible bugs
ONE_DAY = 24 * 3600


def post_user():
    """Create new user"""
    fullname = request.get_json()['fullname']
    email = request.get_json()['email']
    password = request.get_json()['password']
    hash = argon2.hash(password)
    new_user = User(fullname=fullname, email=email, hash=hash)
    try:
        new_user.save()
    except UniqueViolatedError:
        return jsonify(error="Duplicated email address"), 409

    token = secrets.token_urlsafe(32)
    value = {
        'id': new_user.id,
        'email': email,
        'token': token,
        'is_root': new_user.is_root.value
    }
    redis_token_db.set(email, json.dumps(value), ex=ONE_DAY)

    return jsonify(value)


def _delete(user_id):
    if g.user['id'] != user_id:
        """ Only self-delete is permitted"""
        return jsonify(message='Unauthorized request'), 403
    user = User(id=user_id)
    user.delete()
    _delete_token()
    return jsonify(message='ok'), 200


delete_user = login_required(_delete)


def post_token():
    """Check email/password then return a token. Actually, it's the 'login' function"""
    email = request.get_json()['email']
    password = request.get_json()['password']
    user = User.fetchone(email=email)
    if user is None:
        return jsonify(error='email address does not exist'), 401

    hash = user.hash
    if argon2.verify(password, hash):
        g.user = user
        token = secrets.token_urlsafe(32)
        value = {
            'id': user.id,
            'email': email,
            'token': token,
            'is_root': user.is_root.value
        }
        redis_token_db.set(email, json.dumps(value), ex=ONE_DAY)
        return jsonify(value)
    else:
        return jsonify(error='email password mismatch'), 401


def _delete_token():
    email = g.user['email']
    redis_token_db.delete(email)
    return jsonify(message="ok")


delete_token = login_required(_delete_token)
