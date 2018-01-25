from app import app
import unittest
import json
from manage import create_root, delete_user
from typing import Tuple

test_client = app.test_client()

topo = {
    "instances":
        [
            {"id": 0, "type": "Instance",
                "name": "Instance0", "x": 138.015625, "y": 347},
            {"id": 1, "type": "Instance",
                "name": "Instance1", "x": 534.015625, "y": 416}
        ],
    "networks":
        [
            {"id": 0, "type": "NetworkNode", "name": "Network0",
                "x": 409.015625, "y": 105, "cidr": "192.168.1.0/24"}
        ],
    "links":
        [
            {"id": 0, "type": "NetworkLink", "name": "Link0",
             "networkId": 0, "instanceId": 0, "ip": "192.168.1.11"},
            {"id": 1, "type": "NetworkLink", "name": "Link1",
             "networkId": 0, "instanceId": 1, "ip": "192.168.1.12"}
        ]
}


def _login(email: str, password: str) -> Tuple[str, str, str]:
    rv = test_client.post('/auth/tokens/', headers={
        'Content-Type': 'application/json',
    }, data=json.dumps({
        'email': email,
        'password': password
    }))

    json_data = json.loads(rv.data)
    user_id = json_data['id']
    email = json_data['email']
    token = json_data['token']
    return (user_id, email, token)


def _signup_root_user():
    create_root('test_admin@gmail.com', '123','Test admin')
    return _login('test_admin@gmail.com', '123')


def _delete_test_user(email):
    delete_user(email)


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        # root user signup
        self.root_id, self.root_email, self.root_token = _signup_root_user()
        self.password = '123'

    def test_wrong_login(self):
        rv = test_client.post('/auth/tokens/', headers={
            'Content-Type': 'application/json',
        }, data=json.dumps({
            'email': self.root_email,
            'password': '3u12oicpo'
        }))

        assert rv.status_code == 401
        json_data = json.loads(rv.data)
        assert json_data['error'] == 'email password mismatch'

    def tearDown(self):
        _delete_test_user(self.root_email)


class ScenarioTestCase(unittest.TestCase):
    def setUp(self):
        self.user_id, self.email, self.token = _signup_root_user()
        self.password = '123'

    def test_create_get_scenario(self):
        rv = test_client.post('/api/scenarios/', headers={
            'Content-Type': 'application/json',
            'Email': self.email,
            'Authorization': self.token
        }, data=json.dumps({
            "name": "testScenario2",
            "description": "ola",
            "topo": topo,
            "isPublic": True
        }))

        duplicated_rv = test_client.post('/api/scenarios/', headers={
            'Content-Type': 'application/json',
            'Email': self.email,
            'Authorization': self.token
        }, data=json.dumps({
            "name": "testScenario2",
            "description": "ola",
            "topo": {
                "instances": [],
                "networks": [],
                "links": []
            },
            "isPublic": True
        }))

        assert rv.status_code == 200
        json_data = json.loads(rv.data)
        scenario_id = json_data['id']
        assert duplicated_rv.status_code == 409

        rv = test_client.get('/api/scenarios/', headers={
            'Content-Type': 'application/json',
            'Email': self.email,
            'Authorization': self.token
        })
        assert rv.status_code == 200
        json_data = json.loads(rv.data)
        assert len(json_data) == 1
        assert json_data[0]['id'] == scenario_id
        assert json_data[0]['name'] == 'testScenario2'
        assert json_data[0]['description'] == 'ola'

    def tearDown(self):
        _delete_test_user(self.email)


class LabTestCase(unittest.TestCase):
    def setUp(self):
        # Signup manager user
        self.user_id, self.email, self.token = _signup_root_user()
        self.password = '123'

        # POST new scenario
        rv = test_client.post('/api/scenarios/', headers={
            'Content-Type': 'application/json',
            'Email': self.email,
            'Authorization': self.token
        }, data=json.dumps({
            "name": "testScenario2",
            "description": "ola",
            "topo": topo,
            "isPublic": True
        }))
        json_data = json.loads(rv.data)
        self.scenario_id = json_data['id']

    def test_labs(self):
        rv = test_client.post('/api/labs/', headers={
            'Content-Type': 'application/json',
            'Email': self.email,
            'Authorization': self.token
        }, data=json.dumps({
            "name": "testlab",
            "description": "lab description",
            "scenarioId": self.scenario_id
        }))
        assert rv.status_code == 200

    def tearDown(self):
        _delete_test_user(self.email)


class UserAPITestCase(unittest.TestCase):
    """Test case for /api/users/"""

    def setUp(self):
        # root user signup
        self.root_id, self.root_email, self.root_token = _signup_root_user()
        # user signup
        self.user_id, self.email, self.token = _signup_test_user()

    def tearDown(self):
        _delete_test_user(self.root_email)
        _delete_test_user(self.email)
