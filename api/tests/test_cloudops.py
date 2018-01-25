import yaml
from cloudops.configurations import generate_userdata

def test_generate_userdata_password():
    configurations = [
        {
            "name": "Enable password authentication",
            "params": {
                "password": 123
            }
        }
    ]
    user_data = generate_userdata(configurations)

    data = yaml.load(user_data)
    assert (data['ssh_pwauth'] is True)


def test_generate_userdata_two_configs():
    configurations = [
        {
            "name": "Enable password authentication",
            "params": {
                "password": 123
            }
        },
        {
            "name": "shorewall",
            "params": {
                "interfaces_count": 2
            }
        }
    ]
    user_data = generate_userdata(configurations)

    data = yaml.load(user_data)

    assert (data['ssh_pwauth'] is True)
    assert (data['packages'][0] == 'shorewall')

