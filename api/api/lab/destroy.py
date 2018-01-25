from threading import Thread
from cloudops import CloudOps
from models import Lab, CloudConfig, Slice, Instance, Router, NetworkNode

from raven import Client
# Use sentry to send manually caught exceptions
sentry_raven = Client()

class DestroyThread(Thread):
    def __init__(self, lab_id):
        Thread.__init__(self)
        self.lab_id = lab_id

    def run(self):
        try:
            lab = Lab.fetchone(id=self.lab_id)
            lab.update(status='destroying')
            cloudconfig = CloudConfig.fetchone(lab_id=self.lab_id)
            self.cloudops = CloudOps(cloudconfig.provider, cloudconfig.detail)

            for sl in Slice.fetchall(lab_id=lab.id):
                # destroy instances
                instances = Instance.fetchall(slice_id=sl.id)
                for instance in instances:
                    instance.update(status='destroying')
                    self.cloudops.delete_instance(instance.cloud_attrs)
                    instance.delete()

                # destroy routers
                routers = Router.fetchall(slice_id=sl.id)
                for router in routers:
                    router.update(status='destroying')
                    self.cloudops.delete_instance(router.cloud_attrs)
                    router.delete()

                # destroy networks
                networks = NetworkNode.fetchall(slice_id=sl.id)
                for n in networks:
                    n.update(status='destroying')
                    self.cloudops.delete_network(n.cloud_attrs)
                    n.delete()

                # Destroy security group
                self.cloudops.ex_delete_security_group(
                    sl.name, sl.cloud_attrs['sec_group_id'])

            self.cloudops.ex_delete_vpc(cloudconfig.detail)

            # delete the lab
            lab.delete()
        except Exception:
            sentry_raven.captureException()
            lab.update(status='destroyfailed')
