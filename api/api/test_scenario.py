import json
import os

from .scenario import validate_network, validate_topo, validate_instance, validate_router

def test_network_validation():
    conf = {
        "cidr": "10.0.0.0/24",
        "gid": "08b6efa0-ff2c-11e7-8837-b5cf0c12eae1",
        "name": "",
        "type": "NetworkNode",
        "x": 451.34375,
        "y": 223
    }

    valid, errors = validate_network(conf)

    assert valid == False
    assert len(errors) == 1
    assert "Network: name required" == errors[0]

    conf = {
        "cidr": "10.0.0.0/33",
        "gid": "08b6efa0-ff2c-11e7-8837-b5cf0c12eae1",
        "name": "test",
        "type": "NetworkNode",
        "x": 451.34375,
        "y": 223
    }

    valid, errors = validate_network(conf)

    assert valid == False
    assert len(errors) == 1
    assert "not a valid netmask" in errors[0]

def test_instance_validation():
    conf = {
        "gid": "0a5a8d80-ff2c-11e7-8837-b5cf0c12eae1",
        "image": "sdn-controller",
        "name": "SDN Controller",
        "status": None,
        "type": "Instance",
        "x": 173.34375,
        "y": 341
    }

    conf1 = {
        "flavor": None,
        "name": "instance1",
        "image": "sdn-controller",
    }
    valid, errors = validate_instance(conf1)

    assert valid == False
    assert len(errors) == 1
    assert "Instance instance1: flavor required" == errors[0]

    conf2 = {
        "flavor": {
            "name": "Large",
            "ram": 4096
        },
        "name": "instance1",
        "image": None
    }
    valid, errors = validate_instance(conf2)

    assert valid == False
    assert len(errors) == 1
    assert "Instance instance1: image required" == errors[0]

    conf3 = {
        "flavor": {
            "name": "Large",
            "ram": 4096
        },
        "name": None,
        "image": "Ubuntu" 
    }
    valid, errors = validate_instance(conf3)

    assert valid == False
    assert len(errors) == 1
    assert "Instance: name required" == errors[0]

def test_router_validation():
    conf = {
        "gid": "0a5a8d80-ff2c-11e7-8837-b5cf0c12eae1",
        "image": "sdn-controller",
        "name": "SDN Controller",
        "status": None,
        "type": "Instance",
        "x": 173.34375,
        "y": 341
    }

    conf1 = {
        "flavor": None,
        "name": "router1",
        "image": "sdn-controller",
    }
    valid, errors = validate_router(conf1)

    assert valid == False
    assert len(errors) == 1
    assert "Router router1: flavor required" == errors[0]

    conf2 = {
        "flavor": {
            "name": "Large",
            "ram": 4096
        },
        "name": "router1",
        "image": None
    }
    valid, errors = validate_router(conf2)

    assert valid == False
    assert len(errors) == 1
    assert "Router router1: image required" == errors[0]

    conf3 = {
        "flavor": {
            "name": "Large",
            "ram": 4096
        },
        "name": None,
        "image": "Ubuntu" 
    }
    valid, errors = validate_router(conf3)

    assert valid == False
    assert len(errors) == 1
    assert "Router: name required" == errors[0]

def test_link_validation():

    # Load a topo with invalid links information
    with open(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'testdata/invalid-topo1.json')
    ) as f:
        invalid_topo = json.load(f)

    valid, errs = validate_topo(invalid_topo)

    assert valid == False
    assert len(errs) == 6

    assert "Link Network0_Instance1: network required" in errs, \
        "There's a link without network info in the invalid_topo1"

    assert "Link Network0_Instance0: target required" in errs, \
        "There's a link without target info in the invalid_topo1"

    assert "Link backupnet_Router0: No such target that has gid aabbcc" in errs

    assert "Link Network1_mininet-vm: No such network that has gid ddeeff" in errs

    invalid_ip_err = next(filter(lambda e: 'Octet 256 (> 255) not permitted' in e, errs), None)
    assert invalid_ip_err is not None, \
        "There's a link with invalid ip address in the invalid_topo1"

    assert "Link Network0_Router0: ip address 10.0.1.10 is not in cidr 10.0.0.0/24" in errs, \
        "There's a link with ip address not within it's cidr"

def test_topo_validation():
    with open(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'testdata/valid-topo1.json')
    ) as f:
        valid_topo = json.load(f)

    valid, errs = validate_topo(valid_topo)
    assert valid == True

