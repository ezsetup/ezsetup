from flask import request, jsonify, g
from flask_classful import FlaskView, route

from models import Lab, Slice, CloudConfig, Scenario
from cloudops import CloudOps

from auth.models import User
from api import permission_required
from auth.decorators import login_required

from api.lab.deploy import DeployThread
from api.lab.destroy import DestroyThread

from backgroundjobs import queue, jobs

from raven import Client
# Use sentry to send manually caught exceptions
sentry_raven = Client()

class Labs(FlaskView):
    decorators = [login_required, permission_required]

    def post(self):
        name = request.get_json()['name']
        description = request.get_json()['description']
        scenario_id = request.get_json()['scenarioId']
        new_lab = Lab.insert(name=name, description=description, scenario_id=scenario_id,
                      owner_id=g.user['id'], status='inactive')
        return jsonify(id=new_lab.id)

    def index(self):
        """Get labs as a owner"""
        labs = Lab.fetchall(owner_id=g.user['id'])
        ret = []
        for l in labs:
            ret.append({
                'id': l.id,
                'name': l.name,
                'description': l.description,
                'status': l.status,
                'slices': len(Slice.fetchall(lab_id=l.id))
            })
        return jsonify(sorted(ret, key=lambda i: i['id'], reverse=True))

    def get(self, id):
        lab = Lab.fetchone(id=id)
        if lab is None:
            return jsonify(message="Lab doesn't existed"), 410
        if lab.status == 'inactive':
            return jsonify({
                'id': lab.id,
                'name': lab.name,
                'status': lab.status
            })
        else:
            slices = []
            for sl in Slice.fetchall(lab_id=lab.id):
                user = User.fetchone(id=sl.user_id)
                slices.append({
                    'id': sl.id,
                    'name': sl.name,
                    'status': sl.status,
                    'username': user.fullname
                })
            return jsonify({
                'id': lab.id,
                'name': lab.name,
                'status': lab.status,
                'slices': slices,
                'errors': lab.error_msgs
            })

    @route('/<int:id>/deploy', methods=['POST'])
    def deploy(self, id):
        cloudconfig_id = request.get_json()['cloudConfigId']
        users = request.get_json()['users']

        lab = Lab.fetchone(id=id)
        cloudconfig = CloudConfig.fetchone(id=cloudconfig_id)

        lab.update(status='deploying')

        first_job = None
        last_jobs = []
        last_jobs_ids = []

        if cloudconfig.provider == 'AWS':
            first_job = queue.enqueue(jobs.create_vpc, cloudconfig, lab)

        """Chances are you are redeploying a lab, whose slices are already created"""
        slices = Slice.fetchall(lab_id=lab.id)

        """Otherwise, create slices for the lab"""
        if len(slices) == 0:
            for index, user in enumerate(users):
                new_slice = Slice.insert(lab_id=lab.id, status='deploying', user_id=user['id'],
                                         name=lab.name + ' / slice_' + str(index), cloud_attrs={})
                slices.append(new_slice)


        for lab_slice in slices:
            if lab_slice.status == 'deploying':
                scenario = Scenario.fetchone(id=lab.scenario_id)
                topo = scenario.topo
                create_sec_group_job = queue.enqueue(jobs.create_sec_group, cloudconfig, 
                        lab, lab_slice, scenario, depends_on=first_job)

                create_networks_job = queue.enqueue(jobs.create_networks, cloudconfig,
                        lab, lab_slice, topo, depends_on=create_sec_group_job)

                create_sec_group_job_id = create_sec_group_job.get_id()
                create_instances_job = queue.enqueue(jobs.create_instances, cloudconfig,
                        lab, lab_slice, topo, create_sec_group_job_id, depends_on=create_networks_job)

                create_routers_job = queue.enqueue(jobs.create_routers, cloudconfig,
                        lab, lab_slice, topo, create_sec_group_job_id, depends_on=create_instances_job)

                update_allowed_address_pairs_job = queue.enqueue(jobs.update_allowed_address_pairs, cloudconfig,
                        lab_slice, topo, depends_on=create_routers_job)

                set_slice_active_job = queue.enqueue(jobs.set_slice_active,
                        lab_slice, depends_on=update_allowed_address_pairs_job)

                last_jobs.append(set_slice_active_job)
                last_jobs_ids.append(set_slice_active_job.get_id())

        queue.enqueue(jobs.set_lab_active, lab, last_jobs_ids, job_id='set_lab_active', 
                depends_on=last_jobs[-1])
        return jsonify(message="ok")

    @route('/<int:id>/destroy', methods=['POST'])
    def destroy(self, id):
        lab = Lab.fetchone(id=id)
        lab.update(status='destroying')
        cloudconfig = CloudConfig.fetchone(lab_id=id)

        last_jobs = []
        last_jobs_ids = []

        for lab_slice in Slice.fetchall(lab_id=lab.id):

            delete_routers_job = queue.enqueue(jobs.delete_routers, cloudconfig,
                    lab, lab_slice)

            delete_instances_job = queue.enqueue(jobs.delete_instances, cloudconfig,
                    lab, lab_slice, depends_on=delete_routers_job)

            delete_networks_job = queue.enqueue(jobs.delete_networks, cloudconfig,
                    lab, lab_slice, depends_on=delete_instances_job)

            # Destroy security group
            delete_sec_group_job = queue.enqueue(jobs.delete_sec_group, cloudconfig,
                    lab, lab_slice, depends_on=delete_networks_job)

            last_jobs.append(delete_sec_group_job)
            last_jobs_ids.append(delete_sec_group_job.get_id())

        if cloudconfig.provider == 'AWS':
            delete_vpc_job = queue.enqueue(jobs.delete_vpc, cloudconfig, lab)

        queue.enqueue(jobs.delete_lab, lab, last_jobs_ids, depends_on=last_jobs[-1])
        return jsonify(message="ok")
