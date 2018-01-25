from flask import g
from models import UserInfo


def get_user_info():
    """Get user_info from database then assign it to g.user"""
    if 'permission_groups' not in g.user:
        user_info = UserInfo.fetchone(user_id=g.user['id'])
        g.user['permission_groups'] = user_info.permission_groups.value
