import os

from app import app
test_client = app.test_client()

TEST_ADMIN_EMAIL = 'test_admin@gmail.com'
TEST_ADMIN_NAME = 'Test Admin'
TEST_ADMIN_PASSWORD = '123456'

TEST_USER_EMAIL = 'test_user@gmail.com'
TEST_USER_NAME = 'Test User'
TEST_USER_PASSWORD = '000000'

SECURITY_GROUP_RULES = [
    'egress ipv4 tcp 22 0.0.0.0/0',
    'ingress ipv4 tcp 22 0.0.0.0/0',
    'ingress ipv6 tcp 22 2001:0db8:85a3:0000:0000:8a2e:0370:7334/32',
    'ingress ipv4 tcp 8080 10.0.0.1',
    'ingress ipv4 tcp 8080-8090 10.0.0.1',
    'ingress ipv4 tcp 10.0.1.1',
    'ingress ipv4 tcp 8000-8010',
    'ingress ipv4 udp',
]

TOPO = {
    'instances': [
        {'id': 0, 'image': 'Ubuntu 16.04 x64', 'flavor': {"name": "Large", "ram": 4096}, 'type': 'Instance', 'name': 'Instance0', 'x': 138.015625, 'y': 347, 'gid': '1'},
        {'id': 1, 'image': 'Ubuntu 16.04 x64', 'flavor': {"name": "Large", "ram": 4096}, 'type': 'Instance', 'name': 'Instance1', 'x': 534.015625, 'y': 416, 'gid': '2'}
    ],
    'networks': [
        {'id': 0, 'type': 'NetworkNode', 'name': 'Network0', 'x': 409.015625, 'y': 105, 'cidr': '192.168.1.0/24', 'gid': '3'}
    ],
    'links': [
        {'id': 0, 'type': 'NetworkLink', 'name': 'Link0', 'network': {'gid': '3'}, 'target': {'type': 'instance','gid': '1'}, 'ip': '192.168.1.11'},
        {'id': 1, 'type': 'NetworkLink', 'name': 'Link1', 'network': {'gid': '3'}, 'target': {'type': 'instance', 'gid': '2'}, 'ip': '192.168.1.12'}
    ]
}

CLOUD_DETAIL = None

os_username = os.environ.get('OPENSTACK_USERNAME', None)
os_password = os.environ.get('OPENSTACK_PASSWORD', None)
os_authurl = os.environ.get('OPENSTACK_AUTHURL', None)
os_project = os.environ.get('OPENSTACK_PROJECT', None)

if os_username is None or \
    os_password is None or \
    os_authurl is None or \
    os_project is None:
        
    CLOUD_DETAIL = None
else:
    CLOUD_DETAIL = {
      'openstackAuthURL': os_authurl,
      'openstackUser': os_username,
      'openstackPassword': os_password,
      'openstackProject': os_project 
    }

def api_headers(email, token):
    return {
        'Content-Type': 'application/json',
        'Email': email,
        'Authorization': token
    }
