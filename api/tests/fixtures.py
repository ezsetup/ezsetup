import json

import pytest
from typing import Tuple

from manage import create_root, delete_user
from .conf import TEST_ADMIN_EMAIL, TEST_ADMIN_PASSWORD, TEST_ADMIN_NAME, \
    TEST_USER_EMAIL, TEST_USER_PASSWORD, TEST_USER_NAME, \
    test_client


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
    return user_id, email, token


def _signup_root_user():
    create_root(TEST_ADMIN_EMAIL, TEST_ADMIN_PASSWORD, TEST_ADMIN_NAME)
    return _login(TEST_ADMIN_EMAIL, TEST_ADMIN_PASSWORD)


def _signup_test_user():
    create_root(TEST_USER_EMAIL, TEST_USER_PASSWORD, TEST_USER_NAME)
    return _login(TEST_USER_EMAIL, TEST_USER_PASSWORD)


@pytest.fixture
def root_user_fixture():
    """ Create a root user for some tests"""
    user_id, email, token = _signup_root_user()
    yield user_id, email, token

    # Start cleaning up
    print("cleaning root_user_fixture")
    delete_user(email)


