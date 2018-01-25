from flask_classful import FlaskView
from flask import jsonify

from api import permission_required
from auth.decorators import login_required


"""
Q: Why only specify the ram value in flavors?
A: In different setups, the cloud providers/admins may choose a different set of vcpu/ram combinations as the flavors set.
So a 'Small'-1vcpu/1GB of this cloud may be a 'Medium' of another cloud.
Fortunately, the amount of ram is often correlated with the flavor size.
"""
FLAVORS = [
    {
        "name": "Small",
        "ram": 1024
    },
    {
        "name": "Medium",
        "ram": 2048
    },
    {
        "name": "Large",
        "ram": 4096,
    },
    {
        "name": "XLarge",
        "ram": 8192
    }
]

class Flavors(FlaskView):
    decorators = [login_required, permission_required]

    def index(self):
        return jsonify(FLAVORS)
