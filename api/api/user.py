from flask import jsonify, g, request
from passlib.hash import argon2
from flask_classful import route, FlaskView
from models import UserInfo
from auth.models import User
from auth.decorators import login_required
from api import permission_required
from postgrespy import UniqueViolatedError
from postgrespy.queries import Select
from helpers import get_user_info


class Users(FlaskView):
    decorators = [login_required, permission_required]

    def index(self):
        with Select(User, "is_root != TRUE") as select:
            select.execute()
            users = select.fetchall()
        ret = []
        for user in users:
            ret.append({
                'id': user.id,
                'fullname': user.fullname,
                'email': user.email
            })
        return jsonify(sorted(ret, key=lambda i: i['id'], reverse=True))

    def get(self, id):
        return "Get user"

    def post(self):
        """Create new user"""
        fullname = request.get_json()['fullname']
        email = request.get_json()['email']
        password = request.get_json()['password']
        permission_groups = request.get_json()['permissionGroups']
        hash = argon2.hash(password)
        new_user = User(fullname=fullname, email=email,
                        hash=hash, is_root=False)
        try:
            new_user.save()
        except UniqueViolatedError:
            return jsonify(error="Duplicated email address"), 409

        """Create the user info for the new user"""
        user_info = UserInfo(user_id=new_user.id,
                             permission_groups=permission_groups)
        user_info.save()
        return jsonify(message="ok")

    @route('/self')
    def get_self(self):
        get_user_info()
        return jsonify(permissionGroups=g.user['permission_groups'])

    @route('/search', methods=['POST'])
    def search(self):
        search_term = request.get_json()['searchTerm']
        search_term = '%' + search_term + '%'
        with Select(User, "is_root != TRUE AND (email ILIKE %s OR fullname ILIKE %s)") as select:
            select.execute((search_term, search_term))
            ret = select.fetchall()
        return jsonify(
            [
                {
                    'fullname': user.fullname,
                    'id': user.id,
                    'email': user.email
                }
                for user in ret])
