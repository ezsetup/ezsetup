
class Permission:
    def __init__(self, resource_class_name: str, method_name: str) -> None:
        """
        :param resource_class_name: name of the flask-classful.FlaskView class
        :param method_name: name of a method defined in the resource class"""
        self.resource_class_name = resource_class_name
        self.method_name = method_name

    def equals(self, resource_class_name: str, method_name: str) -> bool:
        """Check if the permission equas to allow :method: on :resource_class:
        :param resource_class_name: name of the flask-classful.FlaskView class
        :param method_name: name of a method defined in the resource class"""
        if self.resource_class_name == resource_class_name and self.method_name == method_name:
            return True
        else:
            return False


class PermissionGroup:
    def __init__(self, name):
        self._permissions = []
        self.name = name

    def add(self, resource_class_name, method_name):
        """Add a permission to the group
        :param resource_class_name: name of the flask-classful.FlaskView class
        :param method_name: name of a method defined in the resource class"""
        permission = Permission(resource_class_name, method_name)
        self._permissions.append(permission)

    def contains(self, resource_class_name: str, method_name: str) -> bool:
        """Check if the group contains a particular permission
        :param resource_class: Resource class, a subclass of flask_cp.Resource"""
        for permission in self._permissions:
            if permission.equals(resource_class_name, method_name):
                return True
        return False
