from permission import PermissionGroup
from typing import List
from functools import wraps
from flask import g, jsonify
import sys


"""
Implicit, default permission group
Every user has this permission group by default
It always is checked first in _has_permission"""
default_permissions = PermissionGroup("default")
default_permissions.add("Users", "get_self")
default_permissions.add("Slices", "index")
default_permissions.add("Slices", "get")

# define other permission groups
# NOTE: code smell!!! Only admin needs this permission.
permissions_management = PermissionGroup("permissions")

users_management = PermissionGroup("users")
users_management.add("Users", "post")

labs_management = PermissionGroup("labs")
labs_management.add("Scenarios", "index")
labs_management.add("Labs", "post")
labs_management.add("Labs", "index")
labs_management.add("Labs", "get")
labs_management.add("Labs", "deploy")
labs_management.add("Labs", "destroy")
labs_management.add("Users", "search")
labs_management.add("Users", "index")
labs_management.add("Cloudconfigs", "post")
labs_management.add("Slices", "get")
labs_management.add("Configurations", "index")
labs_management.add("Flavors", "index")

# Additional lab management permissions for Assessment module
labs_management.add("Assessments", "post")
labs_management.add("Assessments", "get")
labs_management.add("Assessments", "index")
labs_management.add("Questions", "post")
labs_management.add("Questions", "get")
labs_management.add("Questions", "index")
labs_management.add("Reports", "post")
labs_management.add("Reports", "get")
labs_management.add("Reports", "index")

scenarios_management = PermissionGroup("scenarios")
scenarios_management.add("Scenarios", "post")
scenarios_management.add("Scenarios", "get")
scenarios_management.add("Scenarios", "index")
scenarios_management.add("Scenarios", "patch")
scenarios_management.add("Flavors", "index")

all_permission_groups = [permissions_management,
                         users_management, labs_management, scenarios_management]


def _get_permission_group(name: str) -> PermissionGroup:
    for group in all_permission_groups:
        if group.name == name:
            return group
    return None


def _has_permission(permission_group_names: List[str], resource_cls_name: str, method_name: str) -> bool:
    # Check the default group first
    if default_permissions.contains(resource_cls_name, method_name):
        return True

    # Check other group
    for name in permission_group_names:
        group = _get_permission_group(name)
        if group is not None and group.contains(resource_cls_name, method_name):
            return True
    return False


def permission_required(f):
    """ Check if a request has a permission on a Resource method
    :param f: the wrapped Resource method"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(g, 'user'):
            """ Make sure that `login_required` has been applied"""
            print(
                '[api.permission_require] Make sure that `login_required` has been applied', file=sys.stderr)
            return jsonify(message="Internal server error"), 500

        resource_cls_name, method_name = f.__qualname__.split('.')

        if _has_permission(g.user['permission_groups'], resource_cls_name, method_name):
            return f(*args, **kwargs)
        else:
            return jsonify(message="User has no permission on method " + f.__qualname__), 405
    return decorated_function


def register(app, resource_classes: List, route_prefix: str):
    """ Register resource views to the Flask app"""
    for view in resource_classes:
        view.register(app, route_prefix=route_prefix)
