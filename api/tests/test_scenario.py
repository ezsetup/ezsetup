"""Test case for /api/scenarios/"""
import json
from .fixtures import root_user_fixture
from .conf import SECURITY_GROUP_RULES, TOPO, test_client, api_headers

def test_create_get_scenario(root_user_fixture):
    user_id, email, token = root_user_fixture

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

    duplicated_rv = test_client.post('/api/scenarios/',
        headers=api_headers(email, token),
        data=json.dumps({
            'name': 'testScenario2',
            'description': 'ola',
            'sgRules': [],
            'topo': {
                'instances': [],
                'networks': [],
                'links': []
            },
            'isPublic': True
        })
    )

    assert rv.status_code == 200
    json_data = json.loads(rv.data)
    scenario_id = json_data['id']
    assert duplicated_rv.status_code == 409

    rv = test_client.get('/api/scenarios/', headers=api_headers(email, token))
    assert rv.status_code == 200
    json_data = json.loads(rv.data)

    testScenario2 = next(filter(lambda x: x['name'] == 'testScenario2', json_data), None)
    assert testScenario2 is not None
    assert testScenario2['id'] == scenario_id
    assert testScenario2['name'] == 'testScenario2'
    assert testScenario2['description'] == 'ola'
    assert testScenario2['sgRules'] == SECURITY_GROUP_RULES
