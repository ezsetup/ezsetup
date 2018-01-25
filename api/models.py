from postgrespy.models import Model
from postgrespy.fields import TextField, IntegerField, BooleanField, JsonBField, EnumField, ArrayField


class Scenario(Model):
    name = TextField()
    description = TextField()
    owner_id = IntegerField()
    is_public = BooleanField()
    topo = JsonBField()

    class Meta:
        table = 'scenarios'


class Lab(Model):
    name = TextField()
    description = TextField()
    owner_id = IntegerField()
    scenario_id = IntegerField()
    status = EnumField()

    class Meta:
        table = 'labs'


class Slice(Model):
    lab_id = IntegerField()
    user_id = IntegerField()
    status = EnumField()
    name = TextField()
    cloud_attrs = JsonBField()

    class Meta:
        table = 'slices'


class LabRequest(Model):
    lab_id = IntegerField()
    user_id = IntegerField()
    request_type = EnumField()
    status = EnumField()

    class Meta:
        table = 'labrequests'

class NetworkNode(Model):
    name = TextField()
    cidr = TextField()
    status = EnumField()
    x = IntegerField()
    y = IntegerField()
    cloud_attrs = JsonBField()
    gid = TextField()
    slice_id = IntegerField()

    class Meta:
        table = 'networks'


class Instance(Model):
    name = TextField()
    public_ip = TextField()
    status = EnumField()
    password = TextField()
    x = IntegerField()
    y = IntegerField()
    gid = TextField()
    links = ArrayField()
    cloud_attrs = JsonBField()
    slice_id = IntegerField()
    configurations = ArrayField()
    image = TextField()
    flavor = JsonBField()

    class Meta:
        table = 'instances'

class Router(Model):
    name = TextField()
    public_ip = TextField()
    status = EnumField()
    password = TextField()
    x = IntegerField()
    y = IntegerField()
    gid = TextField()
    links = ArrayField()
    cloud_attrs = JsonBField()
    slice_id = IntegerField()
    configurations = ArrayField()
    image = TextField()
    flavor = JsonBField()

    class Meta:
        table = 'routers'

class CloudConfig(Model):
    lab_id = IntegerField()
    provider = EnumField()
    detail = JsonBField()

    class Meta:
        table = 'cloudconfigs'


class UserInfo(Model):
    user_id = IntegerField()
    permission_groups = ArrayField()

    class Meta:
        table = 'userinfos'
