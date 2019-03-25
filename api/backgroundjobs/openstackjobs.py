import time
from threading import Thread
import re

from rq.job import JobStatus
from models import Slice, Lab, CloudConfig, NetworkNode, Instance, Router
from auth.models import User
from cloudops import Openstack
from typing import Dict, Any, List, Tuple
from . import queue
from api.lab.helpers import randomword


def create_sec_group(cloudconfig: CloudConfig, lab_id, lab_slice: Slice, scenario):
    try:
        openstack = Openstack(
            cloudconfig.detail['openstackAuthURL'], cloudconfig.detail['openstackProject'],
            cloudconfig.detail['openstackUser'], cloudconfig.detail['openstackPassword'])

        sec_group_id = openstack.create_security_group(lab_slice.name)
        new_cloud_attrs = lab_slice.cloud_attrs
        new_cloud_attrs['sec_group_id'] = sec_group_id
        lab_slice.update(cloud_attrs=new_cloud_attrs.value)
        for rule in scenario.sg_rules.value:
            _add_security_group_rule(openstack, sec_group_id, rule)
        return sec_group_id
    except Exception as ex:
        error_type = 'Create security group error'
        error_msgs = [error_type + ': ' + str(ex)]
        lab = Lab.fetchone(id=lab_id)
        lab.update(status='deployfailed', error_msgs = lab.error_msgs + error_msgs)
        raise Exception(error_type) # Raise exception to not execute the next job in the dependency link

def delete_sec_group(cloudconfig: CloudConfig, lab_id, lab_slice: Slice):
    try:
        openstack = Openstack(
            cloudconfig.detail['openstackAuthURL'], cloudconfig.detail['openstackProject'],
            cloudconfig.detail['openstackUser'], cloudconfig.detail['openstackPassword'])
        if lab_slice.cloud_attrs.get('sec_group_id') is not None:
            openstack.delete_security_group(
                lab_slice.name)
    except Exception as ex:
        error_type = 'Delete security group error'
        error_msgs = [error_type + ': ' + str(ex)]
        lab = Lab.fetchone(id=lab_id)
        lab.update(status='destroyfailed', error_msgs = lab.error_msgs + error_msgs)
        raise Exception(error_type) # Raise exception to not execute the next job in the dependency link

# TODO: move this to awsjobs.py
def create_vpc(cloudconfig: CloudConfig, lab_id):
    """
    try:
        if cloudconfig.provider == 'AWS':
            cloudops = CloudOps(cloudconfig.provider, cloudconfig.detail)
            vpc_id, rt_id, ig_id = cloudops.ex_create_vpc(
                lab.name)
            new_detail = cloudconfig.detail
            new_detail['vpc_id'] = vpc_id
            new_detail['rt_id'] = rt_id
            new_detail['ig_id'] = ig_id
            cloudconfig.update(detail=new_detail.value)
    except Exception as ex:
        error_type = 'Create AWS VPC error'
        error_msgs = [error_type + ': ' + str(ex)]

        lab = Lab.fetchone(id=lab_id)
        lab.update(status='deployfailed', error_msgs = lab.error_msgs + error_msgs)
        raise Exception(error_type) # Raise exception to not execute the next job in the dependency link
    """
    pass

# TODO: move this to awsjobs.py
def delete_vpc(cloudconfig: CloudConfig, lab_id):
    """
    try:
        if cloudconfig.provider == 'AWS':
            cloudops = CloudOps(cloudconfig.provider, cloudconfig.detail)
            cloudops.ex_delete_vpc(cloudconfig.detail)
    except Exception as ex:
        error_type = 'Delete AWS VPC error'
        error_msgs = [error_type + ': ' + str(ex)]

        lab = Lab.fetchone(id=lab_id)
        lab.update(status='destroyfailed', error_msgs = lab.error_msgs + error_msgs)
        raise Exception(error_type) # Raise exception to not execute the next job in the dependency link
    """
    pass
    

def set_lab_active(lab_id, last_jobs_ids):
    if len(last_jobs_ids) > 0:
        timeout = 20
        while True:
            all_completed = True
            for id in last_jobs_ids:
                job = queue.fetch_job(id)
                if job.get_status() != JobStatus.FINISHED:
                    all_completed = False

            if all_completed:
                break
            time.sleep(5)
            timeout = timeout - 5
            if timeout == 0:
                break

        lab = Lab.fetchone(id=lab_id)
        if timeout == 0:
            error_type = 'Time out error when trying to set lab active'
            error_msgs = [error_type]

            lab.update(status='deployfailed', error_msgs = lab.error_msgs + error_msgs)
        else:
            lab.update(status='active', error_msgs=[])

def delete_lab(lab_id, last_jobs_ids):
    if len(last_jobs_ids) > 0:
        timeout = 30
        while True:
            all_completed = True
            for id in last_jobs_ids:
                job = queue.fetch_job(id)
                print(job.get_status())
                if job.get_status() != JobStatus.FINISHED:
                    all_completed = False

            if all_completed:
                break
            time.sleep(5)
            timeout = timeout - 5
            if timeout == 0:
                break
        lab = Lab.fetchone(id=lab_id)
        if timeout == 0:
            error_type = 'Time out error when trying to delete lab'
            error_msgs = [error_type]
            lab.update(status='destroyfailed', error_msgs = lab.error_msgs + error_msgs)
        else:
            lab.delete()

class CreateNetThread(Thread):
    def __init__(self, openstack, net):
        Thread.__init__(self)
        self.openstack = openstack 
        self.net = net
    def run(self):
        attrs = self.openstack.create_network(self.net.name, self.net.cidr)
        self.net.update(cloud_attrs=attrs, status='active')

def create_networks(cloudconfig, lab_id, lab_slice, topo):
    try:
        openstack = Openstack(
            cloudconfig.detail['openstackAuthURL'], cloudconfig.detail['openstackProject'],
            cloudconfig.detail['openstackUser'], cloudconfig.detail['openstackPassword'])
        threads = []
        for n in topo['networks']:
            new_net = NetworkNode.insert(
                name=n['name'], cidr=n['cidr'], status='deploying', x=n['x'], y=n['y'],
                slice_id=lab_slice.id, gid=n['gid'])
            t = CreateNetThread(openstack, new_net)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()
    except Exception as ex:
        error_type = 'Create networks error'
        error_msgs = [error_type + ': ' + str(ex)]

        lab = Lab.fetchone(id=lab_id)
        lab.update(status='deployfailed', error_msgs = lab.error_msgs + error_msgs)
        raise Exception(error_type) # Raise exception to not execute the next job in the dependency link

class DeleteNetworkThread(Thread):
    def __init__(self, openstack, net):
        Thread.__init__(self)
        self.openstack = openstack 
        self.net = net
    def run(self):
        if self.net.status == 'active':
            self.net.update(status='destroying')
            self.openstack.delete_network(self.net.cloud_attrs['id'], 
                    self.net.cloud_attrs['router_id'])
            self.net.delete()

def delete_networks(cloudconfig, lab_id, lab_slice):
    try:
        openstack = Openstack(
            cloudconfig.detail['openstackAuthURL'], cloudconfig.detail['openstackProject'],
            cloudconfig.detail['openstackUser'], cloudconfig.detail['openstackPassword'])
        networks = NetworkNode.fetchall(slice_id=lab_slice.id)
        threads = []
        for net in networks:
            t = DeleteNetworkThread(openstack, net)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
    except Exception as ex:
        error_type = 'Delete networks error'
        error_msgs = [error_type + ': ' + str(ex)]

        lab = Lab.fetchone(id=lab_id)
        lab.update(status='destroyfailed', error_msgs = lab.error_msgs + error_msgs)
        raise Exception(error_type) # Raise exception to not execute the next job in the dependency link

class CreateInstanceThread(Thread):
    def __init__(self, openstack, lab_id, instance, lab_slice, sec_group_id):
        Thread.__init__(self)
        self.lab_id = lab_id
        self.openstack = openstack
        self.instance = instance
        self.lab_slice = lab_slice
        self.sec_group_id = sec_group_id
    def run(self):
        try:
            ips = []
            nets = []
            for l in self.instance.links:
                ips.append(l['ip'])
                net = NetworkNode.fetchone(gid=l['network']['gid'], slice_id=self.lab_slice.id)
                nets.append(net)

            instance = self.instance
            public_ip, attrs = self.openstack.create_instance(
                instance.name, nets, ips, instance.configurations, self.sec_group_id, instance.image, instance.flavor)
            instance.update(status='active', public_ip=public_ip, cloud_attrs=attrs)
        except Exception as ex:
            error_type = 'Create instances error'
            error_msgs = [error_type + ': ' + str(ex)]

            lab = Lab.fetchone(id=self.lab_id)
            lab.update(status='deployfailed', error_msgs = lab.error_msgs + error_msgs)
            raise Exception(error_type + str(error_msgs))

def create_instances(cloudconfig, lab_id, lab_slice, topo, create_sec_group_job_id):
    try:
        openstack = Openstack(
            cloudconfig.detail['openstackAuthURL'], cloudconfig.detail['openstackProject'],
            cloudconfig.detail['openstackUser'], cloudconfig.detail['openstackPassword'])
        sec_group_id = queue.fetch_job(create_sec_group_job_id).result
        # Prepare and save the instance models
        for s in topo['instances']:
            links = _extract_links(s, topo)
            configurations, password = _extract_configurations(lab_id, lab_slice, s, topo)

            Instance.insert(
                name=s['name'],
                status='deploying', x=s['x'], y=s['y'],
                gid=s['gid'], slice_id=lab_slice.id,
                image=s['image'],
                flavor=s['flavor'],
                links=links,
                configurations=configurations,
                password=password
            )

        # Actually deployment
        threads = []
        for instance in Instance.fetchall(slice_id=lab_slice.id):
            t = CreateInstanceThread(openstack, lab_id, instance, lab_slice, sec_group_id)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

    except Exception as ex:
        error_type = 'Create instances error'
        error_msgs = [error_type + ': ' + str(ex)]

        lab = Lab.fetchone(id=lab_id)
        lab.update(status='deployfailed', error_msgs = lab.error_msgs + error_msgs)
        raise Exception(error_type) # Raise exception to not execute the next job in the dependency link

class DeleteInstanceThread(Thread):
    def __init__(self, openstack, lab_id, instance):
        Thread.__init__(self)
        self.lab_id = lab_id
        self.instance = instance
        self.openstack = openstack 

    def run(self):
        try:
            if self.instance.status == 'active':
                self.instance.update(status='destroying')
                self.openstack.delete_instance(self.instance.cloud_attrs['id'])
                self.instance.delete()
        except Exception as ex:
            error_type = 'Delete instances error'
            error_msgs = [error_type + ': ' + str(ex)]
            
            lab = Lab.fetchone(id=self.lab_id)
            lab.update(status='destroyfailed', error_msgs = lab.error_msgs + error_msgs)

def delete_instances(cloudconfig, lab_id, lab_slice):
    try:
        openstack = Openstack(
            cloudconfig.detail['openstackAuthURL'], cloudconfig.detail['openstackProject'],
            cloudconfig.detail['openstackUser'], cloudconfig.detail['openstackPassword'])
        instances = Instance.fetchall(slice_id=lab_slice.id)
        threads = []
        for instance in instances:
            t = DeleteInstanceThread(openstack, lab_id, instance)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
    except Exception as ex:
        error_type = 'Delete instances error'
        error_msgs = [error_type + ': ' + str(ex)]

        lab = Lab.fetchone(id=lab_id)
        lab.update(status='destroyfailed', error_msgs = lab.error_msgs + error_msgs)
        raise Exception(error_type) # Raise exception to not execute the next job in the dependency link

class CreateRouterThread(Thread):
    def __init__(self, openstack, lab_id, router, lab_slice, sec_group_id):
        Thread.__init__(self)
        self.lab_id = lab_id
        self.openstack = openstack
        self.router = router
        self.lab_slice = lab_slice
        self.sec_group_id = sec_group_id
    def run(self):
        try:
            ips = []
            nets = []
            for l in self.router.links:
                ips.append(l['ip'])
                net = NetworkNode.fetchone(gid=l['network']['gid'], slice_id=self.lab_slice.id)
                nets.append(net)

            router = self.router
            public_ip, attrs = self.openstack.create_router(
                router.name, nets, ips, router.configurations, self.sec_group_id, router.image, router.flavor)
            router.update(status='active', public_ip=public_ip, cloud_attrs=attrs)
        except Exception as ex:
            error_type = 'Create routers error'
            error_msgs = [error_type + ': ' + str(ex)]

            lab = Lab.fetchone(id=self.lab_id)
            lab.update(status='deployfailed', error_msgs = lab.error_msgs + error_msgs)

def create_routers(cloudconfig, lab_id, lab_slice, topo, create_sec_group_job_id):
    try:
        openstack = Openstack(
            cloudconfig.detail['openstackAuthURL'], cloudconfig.detail['openstackProject'],
            cloudconfig.detail['openstackUser'], cloudconfig.detail['openstackPassword'])
        sec_group_id = queue.fetch_job(create_sec_group_job_id).result

        routers = topo['routers']

        for s in routers:
            links = _extract_links(s, topo)
            configurations, password = _extract_configurations(lab_id, lab_slice, s, topo)

            Router.insert(
                name=s['name'],
                status='deploying', x=s['x'], y=s['y'],
                gid=s['gid'], slice_id=lab_slice.id,
                image=s['image'],
                flavor=s['flavor'],
                links=links,
                configurations=configurations,
                password=password
            )

        # Actually deployment
        threads = []
        for router in Router.fetchall(slice_id=lab_slice.id):
            t = CreateRouterThread(openstack, lab_id, router, lab_slice, sec_group_id)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

    except Exception as ex:
        error_type = 'Create routers error'
        error_msgs = [error_type + ': ' + str(ex)]

        lab = Lab.fetchone(id=lab_id)
        lab.update(status='deployfailed', error_msgs = lab.error_msgs + error_msgs)
        raise Exception(error_type) # Raise exception to not execute the next job in the dependency link

class DeleteRouterThread(Thread):
    def __init__(self, openstack, lab_id, router):
        Thread.__init__(self)
        self.router = router
        self.openstack = openstack
        self.lab_id = lab_id

    def run(self):
        try:
            if self.router.status == 'active':
                self.router.update(status='destroying')
                self.openstack.delete_instance(self.router.cloud_attrs['id'])
                self.router.delete()
        except Exception as ex:
            error_type = 'Delete routers error'
            error_msgs = [error_type + ': ' + str(ex)]

            lab = Lab.fetchone(id=self.lab_id)
            lab.update(status='destroyfailed', error_msgs = lab.error_msgs + error_msgs)

def delete_routers(cloudconfig, lab_id, lab_slice):
    try:
        openstack = Openstack(
            cloudconfig.detail['openstackAuthURL'], cloudconfig.detail['openstackProject'],
            cloudconfig.detail['openstackUser'], cloudconfig.detail['openstackPassword'])
        routers = Router.fetchall(slice_id=lab_slice.id)
        threads = []
        for router in routers:
            t = DeleteRouterThread(openstack, lab_id, router)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
    except Exception as ex:
        error_type = 'Delete routers error'
        error_msgs = [error_type + ': ' + str(ex)]

        lab = Lab.fetchone(id=lab_id)
        lab.update(status='destroyfailed', error_msgs = lab.error_msgs + error_msgs)
        raise Exception(error_type) # Raise exception to not execute the next job in the dependency link

def update_allowed_address_pairs(cloudconfig, lab_id, lab_slice, topo):
    try:
        openstack = Openstack(
            cloudconfig.detail['openstackAuthURL'], cloudconfig.detail['openstackProject'],
            cloudconfig.detail['openstackUser'], cloudconfig.detail['openstackPassword'])
        mac_regex = '^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
        ip_cidr_regex = '^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4]' \
                        '[0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-' \
                        'f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-' \
                        '5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5' \
                        ']|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}((' \
                        '(:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0' \
                        '-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]' \
                        '{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0' \
                        '-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d' \
                        '|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1' \
                        ',4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d' \
                        '|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1' \
                        '\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(\/[0-9]{1,2})*$'
        for link in topo['links']:
            address_pairs = []
            network = NetworkNode.fetchone(gid=link['network']['gid'], slice_id=lab_slice.id)
            if link['target']['type'].lower() == 'instance':
                device = Instance.fetchone(gid=link['target']['gid'], slice_id=lab_slice.id)
            elif link['target']['type'].lower() == 'router':
                device = Router.fetchone(gid=link['target']['gid'], slice_id=lab_slice.id)
            else:
                continue
            for raw_address_pair in link.get('allowedAddressPairs', []):
                mac_address, ip_address, _ = (raw_address_pair + ',,').split(',', 2)
                if ip_address.strip() == '':
                    ip_address = mac_address
                    mac_address = ''
                if (mac_address == '' or re.match(mac_regex, mac_address.strip())) and re.match(ip_cidr_regex, ip_address.strip()):
                    address_pair = {'ip_address': ip_address}
                    if mac_address != '':
                        address_pair['mac_address'] = mac_address
                    address_pairs.append(address_pair)
            if address_pairs:
                openstack.update_allowed_address_pairs(network, device.cloud_attrs['id'], address_pairs)

    except Exception as ex:
        error_type = 'Update allowed address pairs error'
        error_msgs = [error_type + ': ' + str(ex)]

        lab = Lab.fetchone(id=lab_id)
        lab.update(status='deployfailed', error_msgs = lab.error_msgs + error_msgs)
        raise Exception(error_type) # Raise exception to not execute the next job in the dependency link

def set_slice_active(lab_id, lab_slice):
    try:
        lab_slice.update(status='active')
    except Exception as ex:
        error_type = 'Set slice active error'
        error_msgs = [error_type + ': ' + str(ex)]

        lab = Lab.fetchone(id=lab_id)
        lab.update(status='deployfailed', error_msgs = lab.error_msgs + error_msgs)
        raise Exception(error_type) # Raise exception to not execute the next job in the dependency link


def _add_security_group_rule(openstack: Openstack, security_group_id, rule: str):
    regex = '^\s*(ingress|egress)\s+(ipv4|ipv6)\s+([a-z]+)\s*(?:(\d+(?:' \
            '-\d+)?)?(?:\s|$)+)?(?:((?:(?:(?:[0-9A-Fa-f]{1,4}:){7}(?:[0' \
            '-9A-Fa-f]{1,4}|:))|(?:(?:[0-9A-Fa-f]{1,4}:){6}(?::[0-9A-Fa' \
            '-f]{1,4}|(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[' \
            '0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(?:(?:[0-9A-Fa-f]{1' \
            ',4}:){5}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,2})|:(?:(?:25[0-5]|2' \
            '[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9' \
            ']?\d)){3})|:))|(?:(?:[0-9A-Fa-f]{1,4}:){4}(?:(?:(?::[0-9A-' \
            'Fa-f]{1,4}){1,3})|(?:(?::[0-9A-Fa-f]{1,4})?:(?:(?:25[0-5]|' \
            '2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-' \
            '9]?\d)){3}))|:))|(?:(?:[0-9A-Fa-f]{1,4}:){3}(?:(?:(?::[0-9' \
            'A-Fa-f]{1,4}){1,4})|(?:(?::[0-9A-Fa-f]{1,4}){0,2}:(?:(?:25' \
            '[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d' \
            '\d|[1-9]?\d)){3}))|:))|(?:(?:[0-9A-Fa-f]{1,4}:){2}(?:(?:(?' \
            '::[0-9A-Fa-f]{1,4}){1,5})|(?:(?::[0-9A-Fa-f]{1,4}){0,3}:(?' \
            ':(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]' \
            '\d|1\d\d|[1-9]?\d)){3}))|:))|(?:(?:[0-9A-Fa-f]{1,4}:){1}(?' \
            ':(?:(?::[0-9A-Fa-f]{1,4}){1,6})|(?:(?::[0-9A-Fa-f]{1,4}){0' \
            ',4}:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|' \
            '2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(?::(?:(?:(?::[0-9A-Fa-' \
            'f]{1,4}){1,7})|(?:(?::[0-9A-Fa-f]{1,4}){0,5}:(?:(?:25[0-5]' \
            '|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1' \
            '-9]?\d)){3}))|:))|(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)' \
            '\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0' \
            '-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0' \
            '-9][0-9]?))(?:\/[0-9]{1,2})?(\s|$)))*'

    matches = re.finditer(regex, rule)

    query = None
    for _, match in enumerate(matches):
        query = {}
        for group_id, segment in enumerate(match.groups()):
            group_id += 1
            if group_id == 1:
                query['direction'] = segment
            elif group_id == 2:
                ethertype = segment
                query['ethertype'] = ethertype[:2].upper() + ethertype[2:]
            elif group_id == 3:
                query['protocol'] = segment
            elif group_id == 4:
                port = segment
                if port is None:
                    query['port_range_max'] = None
                    query['port_range_min'] = None
                else:
                    range = port.split('-')
                    query['port_range_max'] = query['port_range_min'] = range[0]
                    if len(range) == 2:
                        query['port_range_max'] = range[1]
            elif group_id == 5:
                query['remote_ip_prefix'] = segment
        break

    if query is not None:
        openstack.create_security_group_rule(security_group_id, **query)

def _extract_links(instance: Dict[str, Any], topo: Dict[str, Any]) -> List:
    """extract links attached to an instance base on the topology"""
    links = []
    for l in topo['links']:
        if l['target']['gid'] == instance['gid']:
            links.append(l)
    return links


def _extract_configurations(lab_id, slice: Slice, instance: Dict[str, Any], topo: Dict[str, Any]) \
        -> Tuple[List[Dict[str, Any]], str]:
    """extract configurations of an instance base on the topology
    the extracted configurations is a dict of configuration name ('name') and and rendering parameters ('params')
    rendering parameters can be None"""

    lab = Lab.fetchone(id=lab_id)
    configurations = []

    # configurations.append({"name": "staticroute", "params": _extract_static_route(instance, topo)})
    configurations.append({"name": "add-local-host", "params": {}})

    if instance.get('type') == "Router":
        """ Get the number of interfaces """
        interfaces_count = sum(1 for link in topo['links'] if link['target']['gid'] == instance['gid'])
        configurations.append({"name": "shorewall", "params": {"interfaces_count": interfaces_count}})

    password = None

    for conf in instance.get('configurations', []):
        params : Dict[str, Any] = {}
        if conf == "Enable password authentication" or conf == "noVNC":
            if password is None:
                password = randomword(8)
            params['password'] = password
        elif conf == "grr-client":
            user = User.fetchone(id=slice.user_id)
            params['labels'] = [lab.name, user.email, instance['name']]

        configurations.append({"name": conf, "params": params})

    return configurations, password


def _extract_static_route(instance: Dict[str, Any], topo: Dict[str, Any]) -> Dict[str, Any] :
    """Extract static route for an instance / router instance
    - TODO: implement me
    - TODO: check if _extract_static_route works with cases where there are more than one routers connected to an instance,
    in these cases, more than one static routes might be used
    the current code might work, but it needs to be checked anyway"""

    # get the networks to which the instance is connected
    connected_nets = []
    for link in topo['links']:
        if link['target']['gid'] == instance['gid']:
            connected_nets.append(link['network'])

    for net in connected_nets:
        # TODO: find the all routers, exclude the instance (if the instance is also a router)
        # routers = []
        pass


    # for each network, get the ip of the router and directly/indirectly connected cidrs

    return None
