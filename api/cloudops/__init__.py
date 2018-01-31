from enum import Enum
from time import sleep
import base64

from typing import Tuple, Optional

from openstack import connection
from openstack.exceptions import HttpException

import boto3
from botocore.exceptions import ClientError

from cloudops.configurations import generate_userdata


class CloudProvider(Enum):
    OPENSTACK = 'Openstack'
    AWS = 'AWS'
    GCLOUD = 'GCloud'
    AZURE = 'Azure'


class CloudOps(object):
    def __init__(self, provider_name: str, detail) -> None:
        self.provider = CloudProvider(provider_name)  # Access enum by value
        if self.provider == CloudProvider.OPENSTACK:
            self.openstack = Openstack(
                detail['openstackAuthURL'], detail['openstackProject'],
                detail['openstackUser'], detail['openstackPassword'])
        if self.provider == CloudProvider.AWS:
            self.aws = AWS(
                detail['awsAccessKeyId'],
                detail['awsSecretAccessKey'],
                detail['awsRegion']
            )

    def test_connection(self) -> bool:
        """Test the cloud connection and the credentials"""
        if self.provider == CloudProvider.OPENSTACK:
            return self.openstack.test_connection()
        if self.provider == CloudProvider.AWS:
            return self.aws.test_connection()
        else:
            return None

    def create_network(self, name, cidr) -> object:
        if self.provider == CloudProvider.OPENSTACK:
            return self.openstack.create_network(name, cidr)
        if self.provider == CloudProvider.AWS:
            return self.aws.create_subnet(name, cidr)
        else:
            return None

    def delete_network(self, attrs: dict):
        if self.provider == CloudProvider.OPENSTACK:
            self.openstack.delete_network(attrs['id'], attrs['router_id'])
        if self.provider == CloudProvider.AWS:
            self.aws.delete_subnet(attrs['id'])

    def create_instance(self, name, networks, ips, configurations, sec_group_id, image_name: str, flavor: dict) -> Tuple[str, object]:
        """Return (public_ip, cloud_attrs)"""
        # Prepare user-data based on configurations list
        userdata = generate_userdata(configurations)

        # Create the instance
        if self.provider == CloudProvider.OPENSTACK:
            public_ip, cloud_attrs = self.openstack.create_instance(name, networks, ips, userdata, sec_group_id, image_name, flavor)
        if self.provider == CloudProvider.AWS:
            # TODO: implement flavor for AWS instance
            public_ip, cloud_attrs = self.aws.create_instance(name, networks, ips, userdata, sec_group_id, image_name)

        return public_ip, cloud_attrs

    def create_router(self, name, networks, ips, configurations, sec_group_id, image_name: str, flavor: dict) -> Tuple[str, object]:
        # Prepare user-data based on configurations list
        configurations.append("shorewall")
        userdata = generate_userdata(configurations)

        if self.provider == CloudProvider.OPENSTACK:
            public_ip, cloud_attrs = self.openstack.create_router(name, networks, ips, userdata, sec_group_id, image_name, flavor)
        if self.provider == CloudProvider.AWS:
            # TODO: implement flavor for AWS router
            public_ip, cloud_attrs = self.aws.create_router(name, networks, ips, userdata, sec_group_id)

        return public_ip, cloud_attrs
    
    def delete_instance(self, attrs: dict):
        if self.provider == CloudProvider.OPENSTACK:
            self.openstack.delete_instance(attrs['id'])
        if self.provider == CloudProvider.AWS:
            self.aws.delete_instance(attrs['id'])

    def ex_create_vpc(self, name: str):
        '''For AWS only'''
        if self.provider == CloudProvider.AWS:
            return self.aws.create_vpc(name)

    def ex_delete_vpc(self, cloud_detail: dict):
        '''For AWS only'''
        if self.provider == CloudProvider.AWS:
            self.aws.delete_vpc(
                cloud_detail['vpc_id'], cloud_detail['rt_id'], cloud_detail['ig_id'])

    def ex_create_security_group(self, name: str) -> Optional[str]:
        ''' Create a security group that allows ping, ssh, internal
        Available for Openstack (and possibly AWS) only'''
        if self.provider == CloudProvider.OPENSTACK:
            return self.openstack.create_security_group(name)
        if self.provider == CloudProvider.AWS:
            return self.aws.create_security_group(name)
        return None

    def ex_delete_security_group(self, name: str, id: str) -> None:
        if self.provider == CloudProvider.OPENSTACK:
            self.openstack.delete_security_group(name)
        if self.provider == CloudProvider.AWS:
            self.aws.delete_security_group(id)


class Openstack(object):
    def __init__(self, auth_url, project_name, username, password, keystone_version=None,
                 project_domain_name='default', user_domain_name='default') -> None:
        """create connection object that holds the openstack connection
        http://developer.openstack.org/sdks/python/openstacksdk/users/connection.html
        """

        # Get keystone_version from auth_url
        if keystone_version is None:
            if '/v2' in auth_url:
                keystone_version = 'v2'
            if '/v3' in auth_url:
                keystone_version = 'v3'

        if keystone_version == 'v2':
            auth_args = {
                'auth_url': auth_url,
                'project_name': project_name,
                'username': username,
                'password': password}
        else:
            auth_args = {
                'auth_url': auth_url,
                'project_name': project_name,
                'username': username,
                'password': password,
                'project_domain_name': project_domain_name,
                'user_domain_name': user_domain_name}
        self.conn = connection.Connection(**auth_args)

    def test_connection(self) -> bool:
        try:
            token = self.conn.authorize()
            """ TODO: Check how long this token exists. If forever, we can use it for future autorization
            without storing cloud credentials.
            However, I think it doens't exist too long"""
            return True
        except HttpException:
            return False
        except Exception as ex:
            print('cloudops.Openstack::test_connection - Unexpected exception ', ex)
            return False

    def create_security_group(self, name: str):
        conn = self.conn
        sec_group = conn.network.find_security_group(name)
        if sec_group is None:
            sec_group = conn.network.create_security_group(
                name=name)

        # enable ping and rules
        ping_ipv4_rules = conn.network.security_group_rules(
            security_group_id=sec_group.id,
            protocol='icmp')

        if next(ping_ipv4_rules, None) is None:
            conn.network.create_security_group_rule(
                security_group_id=sec_group.id,
                direction='ingress', remote_ip_prefix='0.0.0.0/0',
                protocol='icmp', port_range_max=None,
                port_range_min=None, ethertype='IPv4')

        # allow ssh
        ssh_ipv4_rules = conn.network.security_group_rules(
            security_group_id=sec_group.id,
            protocol='tcp', port_range_max=22, port_range_min=22,
            direction='ingress', remote_ip_prefix='0.0.0.0/0')

        if next(ssh_ipv4_rules, None) is None:
            conn.network.create_security_group_rule(
                security_group_id=sec_group.id,
                direction='ingress', remote_ip_prefix='0.0.0.0/0',
                protocol='tcp', port_range_max=22,
                port_range_min=22, ethertype='IPv4')

        # allow internal, same group (slice) tcp connections
        internal_tcp_ipv4_rules = conn.network.security_group_rules(
            security_group_id=sec_group.id, direction='ingress',
            ethertype='IPv4', remote_group_id=sec_group.id
        )

        if next(internal_tcp_ipv4_rules, None) is None:
            conn.network.create_security_group_rule(
                security_group_id=sec_group.id, direction='ingress',
                ethertype='IPv4', remote_group_id=sec_group.id
            )

        # allow port 6080
        try:
            conn.network.create_security_group_rule(
                    security_group_id=sec_group.id, direction='ingress', remote_ip_prefix='0.0.0.0/0',
                    protocol='tcp', port_range_max=6080, port_range_min=6080,
                    ethertype='IPv4')
        except HttpException as ex:
            if not "Security group rule already exists" in ex.message:
                raise ex

        return sec_group.id

    def delete_security_group(self, name):
        conn = self.conn
        sec_group = conn.network.find_security_group(name)
        if sec_group is not None:
            conn.network.delete_security_group(sec_group)

    def create_network(self, name, subnet_cidr) -> object:
        """Create a network with single subnet.
        Openstack network can contain more than one subnets.
        For simplicity, this function creates a network with a single subnet only.
        :param name: name of the network.
        :param subnet_cidr: cidr of the subnet.
            For example: subnet_cidr='192.168.1.1/24'
        :returns: :class: `openstack.network.v2.network.Network`
        `http://developer.openstack.org/sdks/python/openstacksdk/users/resources/network/v2/network.html#openstack.network.v2.network.Network`
        """
        conn = self.conn
        net = conn.network.create_network(name=name)

        subnet = conn.network.create_subnet(
            name=name + '_subnet',
            network_id=net.id,
            ip_version='4',
            cidr=subnet_cidr,
            dns_nameservers=['8.8.8.8', '8.8.4.4'])

        net = conn.network.find_network(net.id)
        ext_net = conn.network.find_network('ext-net')
        router = conn.network.create_router(
            name=name + '_internal_router', external_gateway_info={'network_id': ext_net.id}
        )
        conn.network.add_interface_to_router(router, subnet.id)

        return {
            'provider': 'Openstack',
            'id': net.id,
            'router_id': router.id
        }

    def delete_network(self, net_id, router_id):
        conn = self.conn
        ports = conn.network.ports(
            network_id=net_id, device_id=router_id
        )
        for p in ports:
            conn.network.remove_interface_from_router(
                router_id, port_id=p.id
            )
            conn.network.delete_port(p)
        conn.network.delete_router(router_id)
        sleep(2)
        conn.network.delete_network(net_id)
        sleep(2)

    def _find_flavor(self, **kwargs):
        """Find flavor by providing requirements like ram, vcpus"""
        ret = None
        conn = self.conn
        flavors = conn.compute.flavors()

        for f in flavors:
            found = True
            for k, v in kwargs.items():
                if getattr(f, k) != v:
                    found = False
                    break
            if found:
                ret = f
                break

        # TODO: if ret is None, show error that there's no flavor sastifies requirements
        # TODO: or better, find the closes flavor that satisfies requirements
        return ret


    def create_instance(self, name, networks, ips, user_data, sec_group_id, image_name, flavor_dict: dict) -> Tuple[str, object]:
        """Return (public_ip, cloud_attrs)"""
        conn = self.conn
        image = conn.compute.find_image(image_name)
        # TODO: implement log stream, and show error log if no image found

        flavor = self._find_flavor(ram=flavor_dict['ram'])

        bytes_data = user_data.encode('utf-8')
        encoded = base64.b64encode(bytes_data)
        user_data = encoded.decode('utf-8')
        instance = conn.compute.create_server(
            name=name, image_id=image.id,
            flavor_id=flavor.id,
            user_data=user_data,
            networks=[{"uuid": net.cloud_attrs['id'], "fixed_ip": ip}
                      for net, ip in zip(networks, ips)]
        )

        instance = conn.compute.wait_for_server(instance)

        """ Remove instance from the default security groups, then add instance to the correct security group
            WHY? the openstacksdk always add new instances to 'default' security group, 
        even if I specify the `sec_groups` option"""

        project_id = instance.project_id
        default_sec_groups = conn.network.security_groups(
            name='default', project_id=project_id)
        for default_sec_group in default_sec_groups:
            conn.compute.remove_security_group_from_server(
                instance, default_sec_group)

        sec_group = conn.network.find_security_group(sec_group_id)
        conn.compute.add_security_group_to_server(instance, sec_group)

        # available ips that are DOWN a.k.a not being used
        ext_net = conn.network.find_network('ext-net')
        available_ips = conn.network.ips(
            floating_network_id=ext_net.id, project_id=project_id, status='DOWN')
        ip = next(available_ips, None)
        if ip is None:
            ip = conn.network.create_ip(
                floating_network_id=ext_net.id, project_id=project_id)
        conn.compute.add_floating_ip_to_server(
            instance, ip.floating_ip_address)

        return ip.floating_ip_address, {
            'provider': 'Openstack',
            'id': instance.id
        }

    def create_router(self, name, networks, ips, user_data, sec_group_id, image_name: str, flavor_dict: dict)-> Tuple[str, object]:
        conn = self.conn
        image = conn.compute.find_image(image_name)
        # TODO: log error to log stream if image is None
        print('image for router: ', image)

        flavor = self._find_flavor(ram=flavor_dict['ram'])

        bytes_data = user_data.encode('utf-8')
        encoded = base64.b64encode(bytes_data)
        user_data = encoded.decode('utf-8')

        instance = conn.compute.create_server(
            name=name, image_id=image.id,
            flavor_id=flavor.id,
            user_data=user_data,
            networks=[{"uuid": net.cloud_attrs['id'], "fixed_ip": ip}
                      for net, ip in zip(networks, ips)]
        )

        instance = conn.compute.wait_for_server(instance)

        """ Remove instance from the default security groups, then add instance to the correct security group
            WHY? the openstacksdk always add new instances to 'default' security group, 
        even if I specify the `sec_groups` option"""

        project_id = instance.project_id
        default_sec_groups = conn.network.security_groups(
            name='default', project_id=project_id)
        for default_sec_group in default_sec_groups:
            conn.compute.remove_security_group_from_server(
                instance, default_sec_group)

        sec_group = conn.network.find_security_group(sec_group_id)
        conn.compute.add_security_group_to_server(instance, sec_group)

        # available ips that are DOWN a.k.a not being used
        ext_net = conn.network.find_network('ext-net')
        available_ips = conn.network.ips(
            floating_network_id=ext_net.id, project_id=project_id, status='DOWN')
        float_ip = next(available_ips, None)
        if float_ip is None:
            float_ip = conn.network.create_ip(
                floating_network_id=ext_net.id, project_id=project_id)
        conn.compute.add_floating_ip_to_server(
            instance, float_ip.floating_ip_address)

        # Allow every other net on a port
        for net, ip in zip(networks, ips):
            # find the port
            query = conn.network.ports(network_id=net.cloud_attrs['id'], device_id=instance.id)
            port = next(query, None)

            # find every other net
            other_nets = [n for n in networks if n != net]

            # update the port
            conn.network.update_port(port, allowed_address_pairs=[{"ip_address": net.cidr} for net in other_nets])


        return float_ip.floating_ip_address, {
            'provider': 'Openstack',
            'id': instance.id
        }
    def delete_instance(self, id):
        self.conn.compute.delete_server(id)
        while (self.conn.compute.find_server(id)) is not None:
            sleep(2)


class AWS(object):
    def __init__(self, key_id, secret, region):
        self.ec2 = boto3.resource('ec2', aws_access_key_id=key_id,
                                  aws_secret_access_key=secret,
                                  region_name=region)

    def test_connection(self) -> bool:
        try:
            list(self.ec2.vpcs.all())
            return True
        except ClientError as err:
            print(err)
            return False

    def create_vpc(self, name: str, cidr='192.168.0.0/16') -> Tuple[str, str, str]:
        self.vpc = self.ec2.create_vpc(CidrBlock=cidr)
        self.vpc.create_tags(Tags=[{"Key": "Name", "Value": name}])
        self.vpc.wait_until_available()

        # create then attach internet gateway
        self.ig = self.ec2.create_internet_gateway()
        self.vpc.attach_internet_gateway(InternetGatewayId=self.ig.id)

        # create a route table and a public route
        self.route_table = self.vpc.create_route_table()
        self.route_table.create_route(
            DestinationCidrBlock='0.0.0.0/0',
            GatewayId=self.ig.id
        )
        return self.vpc.id, self.route_table.id, self.ig.id

    def delete_vpc(self, vpc_id: str, rt_id: str, ig_id: str):
        rt = self.ec2.RouteTable(rt_id)
        rt.delete()
        ig = self.ec2.InternetGateway(ig_id)
        ig.detach_from_vpc(VpcId=vpc_id)
        ig.delete()
        vpc = self.ec2.Vpc(vpc_id)
        vpc.delete()

    def create_security_group(self, name: str):
        sec_group = self.ec2.create_security_group(
            GroupName=name, Description=name + ' security group', VpcId=self.vpc.id)

        sec_group.authorize_ingress(
            CidrIp='0.0.0.0/0',
            IpProtocol='icmp',
            FromPort=-1,
            ToPort=-1
        )

        # allow all ingress from same group
        sec_group.authorize_ingress(
            IpPermissions=[
                {
                    "IpProtocol": "tcp",
                    "FromPort": 0,
                    "ToPort": 65535,
                    "UserIdGroupPairs": [{
                        "GroupId": sec_group.id,
                        "VpcId": self.vpc.id
                    }]
                },
                {
                    "IpProtocol": "udp",
                    "FromPort": 0,
                    "ToPort": 65535,
                    "UserIdGroupPairs": [{
                        "GroupId": sec_group.id,
                        "VpcId": self.vpc.id
                    }]
                }
            ]
        )
        # allow all ssh
        sec_group.authorize_ingress(
            CidrIp='0.0.0.0/0',
            IpProtocol='tcp',
            FromPort=22,
            ToPort=22
        )

        # TODO: open tcp 6080 port for noVNC
        return sec_group.id

    def delete_security_group(self, id: str):
        sec_group = self.ec2.SecurityGroup(id)
        sec_group.delete()

    def create_subnet(self, name: str, cidr: str) -> object:
        subnet = self.ec2.create_subnet(CidrBlock=cidr, VpcId=self.vpc.id)
        self.route_table.associate_with_subnet(SubnetId=subnet.id)
        return {
            'provider': 'AWS',
            'id': subnet.id
        }

    def delete_subnet(self, id: str):
        subnet = self.ec2.Subnet(id)
        subnet.delete()

    def create_instance(self, name, networks, ips, userdata, sec_group_id, image_name, enable_routing=False, flavor_name='t2.micro') -> Tuple[str, object]:
        """Return (public_ip, cloud_attrs)"""

        # find ami id by image_name
        images = self.ec2.images.filter(Filters=[{
            'Name': 'name',
            'Values': [image_name]
        }])

        if len(list(images)) > 0:
            ami_id = list(images)[0].id

        network_interfaces = []
        index = 0
        for net, ip in zip(networks, ips):
            network_interfaces.append({
                'SubnetId': net.cloud_attrs['id'],
                'DeviceIndex': index,
                'AssociatePublicIpAddress': True,
                'Groups': [sec_group_id],
                'PrivateIpAddress': ip
            })
            index = index + 1

        # TODO: handle exception when ami_id is None
        
        # Unlike in Openstack, UserData is just string in AWS
        instances = self.ec2.create_instances(
            ImageId=ami_id, InstanceType=flavor_name, MaxCount=1, MinCount=1,
            NetworkInterfaces=network_interfaces,
            UserData=userdata)
        instances[0].wait_until_running()
        instance = self.ec2.Instance(instances[0].id)
        return instance.public_ip_address, {
            'provider': 'AWS',
            'id': instance.id
        }

    def delete_instance(self, id: str):
        instance = self.ec2.Instance(id)
        instance.terminate()
        instance.wait_until_terminated()

    def create_router(self, name, networks, ips, userdata, sec_group_id):
        # TODO: implement me
        pass
