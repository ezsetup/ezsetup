"""Test case for /api/tokens/"""
import json
from .fixtures import root_user_fixture, test_client
from .conf import TEST_ADMIN_PASSWORD, test_client

def test_correct_login(root_user_fixture):
    user_id, email, token = root_user_fixture
    rv = test_client.post('/auth/tokens/', headers={
        'Content-Type': 'application/json',
    }, data=json.dumps({
        'email': email,
        'password': TEST_ADMIN_PASSWORD
    }))
    assert rv.status_code == 200
    json_data = json.loads(rv.data)
    assert json_data['email'] == email

def test_wrong_login(root_user_fixture):
    user_id, email, token = root_user_fixture
    rv = test_client.post('/auth/tokens/', headers={
        'Content-Type': 'application/json',
    }, data=json.dumps({
        'email': email,
        'password': '3u12oicpo'
    }))

    assert rv.status_code == 401
    json_data = json.loads(rv.data)
    assert json_data['error'] == 'email password mismatch'
