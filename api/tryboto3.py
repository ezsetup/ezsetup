import boto3
import os

# http://boto3.readthedocs.io/en/latest/reference/services/ec2.html#service-resource

ec2 = boto3.resource('ec2', aws_access_key_id='AKIAIWX4NFSUSIX2W3LA',
                     aws_secret_access_key='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',
                     region_name='us-west-2')

# Find image by name
images = ec2.images.filter(Filters=[{
    'Name': 'name',
    'Values': ['Kali-2016.1-64bit']
}])

if len(list(images)) > 0:
    print(list(images)[0].id)
# create VPC
vpc = ec2.create_vpc(CidrBlock='192.168.0.0/16')
vpc.wait_until_available()
# we can assign a name to vpc, or any resource, by using tag
vpc.create_tags(Tags=[{"Key": "Name", "Value": "deleteme_vpc"}])
vpc.wait_until_available()
print(vpc.id)

# create then attach internet gateway
ig = ec2.create_internet_gateway()
vpc.attach_internet_gateway(InternetGatewayId=ig.id)
print(ig.id)

# create a route table and a public route
route_table = vpc.create_route_table()
route = route_table.create_route(
    DestinationCidrBlock='0.0.0.0/0',
    GatewayId=ig.id
)
print(route_table.id)

# create subnet
subnet = ec2.create_subnet(CidrBlock='192.168.1.0/24', VpcId=vpc.id)
print(subnet.id)

# associate the route table with the subnet
route_table.associate_with_subnet(SubnetId=subnet.id)

# Create sec group
sec_group = ec2.create_security_group(
    GroupName='slice_0', Description='slice_0 sec group', VpcId=vpc.id)
sec_group.authorize_ingress(
    CidrIp='0.0.0.0/0',
    IpProtocol='icmp',
    FromPort=-1,
    ToPort=-1
)
sec_group.authorize_ingress(
    IpPermissions=[
        {
            "IpProtocol": "tcp",
            "FromPort": 0,
            "ToPort": 65535,
            "UserIdGroupPairs": [{
                "GroupId": sec_group.id,
                "VpcId": vpc.id
            }]
        },
        {
            "IpProtocol": "udp",
            "FromPort": 0,
            "ToPort": 65535,
            "UserIdGroupPairs": [{
                "GroupId": sec_group.id,
                "VpcId": vpc.id
            }]
        }
    ]
)
print(sec_group.id)

"""
# find image id ami-835b4efa / us-west-2
# Create instance
instances = ec2.create_instances(
    ImageId='ami-835b4efa', InstanceType='t2.micro', MaxCount=1, MinCount=1,
    NetworkInterfaces=[{'SubnetId': subnet.id, 'DeviceIndex': 0, 'AssociatePublicIpAddress': True, 'Groups': [sec_group.group_id]}])
instances[0].wait_until_running()
print(instances[0].id)

# Terminate instance
instance = ec2.Instance(instances_id)
instance.terminate()

# delete sec group
sec_group2 = ec2.SecurityGroup(sec_group_id)
sec_group2.delete()

# delete subnet
subnet2 = ec2.Subnet(subnet_id)
subnet2.delete()
# delete vpc
vpc2 = ec2.Vpc(vpc_id)
vpc2.delete()
"""
