from passlib.hash import argon2
from auth.models import User
from models import UserInfo
from postgrespy import UniqueViolatedError
from api import all_permission_groups


def create_root(email, password, fullname):
    hash = argon2.hash(password)
    new_root = User(fullname=fullname, email=email, hash=hash, is_root=True)
    try:
        new_root.save()
    except UniqueViolatedError:
        print('Duplicated root user')
    root = User.fetchone(email=email)
    root_info = UserInfo(user_id=root.id, permission_groups=[
                         group.name for group in all_permission_groups])
    root_info.save()


def delete_user(email):
    user = User.fetchone(email=email)
    if user is not None:
        user.delete()
