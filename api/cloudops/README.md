## Myopenstack

Requirement: `openstacksdk`

Openstacksdk: http://developer.openstack.org/sdks/python/openstacksdk/users/index.html

Helper functions for working with Openstack SDK

To use this module, simply call functions in `instance.py`, `network.py` after setting some Openstack environment variables. These variables include:

- OPENSTACK_AUTH_URL
- OPENSTACK_PROJECT
- OPENSTACK_USERNAME
- OPENSTACK_PASSWORD
- OPENSTACK_FLAVOR=m1.small
- OPENSTACK_IMAGE=CC-Ubuntu14.04
- OPENSTACK_KEYPAIR