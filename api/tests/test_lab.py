"""Test case for /api/labs/"""
import time
import json
import pytest

from .fixtures import root_user_fixture
from .conf import test_client, api_headers, SECURITY_GROUP_RULES, TOPO, CLOUD_DETAIL

from models import Lab

@pytest.fixture
def post_scenario(root_user_fixture):
    user_id, email, token = root_user_fixture

    # POST new scenario
    rv = test_client.post('/api/scenarios/', 
        headers=api_headers(email, token),
        data=json.dumps({
            'name': 'testScenario2',
            'description': 'ola',
            'sgRules': SECURITY_GROUP_RULES,
            'topo': TOPO,
            'isPublic': True
        })
    )
    json_data = json.loads(rv.data)
    scenario_id = json_data['id']

    return scenario_id

@pytest.fixture
def post_lab(post_scenario, root_user_fixture):

    scenario_id = post_scenario
    user_id, email, token = root_user_fixture
    # Create a lab
    rv = test_client.post('/api/labs/', 
        headers=api_headers(email, token),
        data=json.dumps({
            'name': 'testlab',
            'description': 'lab description',
            'scenarioId': scenario_id
        })
    )
    assert rv.status_code == 200
    json_data = json.loads(rv.data)
    lab_id = json_data['id']
    return lab_id



@pytest.mark.skipif(CLOUD_DETAIL is None, reason='No cloud detail is provided')
def test_deploy_destroy_lab(post_lab, root_user_fixture):
    user_id, email, token = root_user_fixture
    lab_id = post_lab
    # Create a cloud config
    rv = test_client.post('/api/cloudconfigs/', 
        headers=api_headers(email, token),
        data=json.dumps({
            'cloudDetail': CLOUD_DETAIL,
            'provider': 'Openstack',
            'labId': lab_id
        })
    )
    assert rv.status_code == 200

    cloudconfig_id = json.loads(rv.data)['id']
    users = [{'id': user_id}]

    deploy_url = '/api/labs/{0}/deploy'.format(lab_id,)
    rv = test_client.post(deploy_url, 
        headers=api_headers(email, token),
        data=json.dumps({
            'cloudConfigId': cloudconfig_id,
            'users': users
        })
    )
    assert rv.status_code == 200

    # assert lab is active after a while
    timeout = 200
    while True:
        lab = Lab.fetchone(id=lab_id)
        if lab.status == 'active':
            break
        print(lab.status)
        print(lab.error_msgs)
        assert lab.status != 'deployfailed'
        time.sleep(20)
        timeout = timeout - 20
        if timeout <= 0:
            break
    assert timeout > 0, "Deployment timeout"

    

    # destroy lab
    destroy_url = '/api/labs/{0}/destroy'.format(lab_id,)
    rv = test_client.post(destroy_url,
        headers={
            'Content-Type': 'application/json',
            'Email': email,
            'Authorization': token
        })
            
    timeout = 200
    while True:
        lab = Lab.fetchone(id=lab_id)
        if lab is None:
            break
        print(lab.status)
        print(lab.error_msgs)
        assert lab.status != 'destroyfailed'
        time.sleep(20)
        timeout = timeout - 20
        if timeout <= 0:
            break
    assert timeout > 0, "Deletion timeout"
