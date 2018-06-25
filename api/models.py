from postgrespy.models import Model
from postgrespy.fields import TextField, IntegerField, BooleanField, JsonBField, EnumField, ArrayField


class Scenario(Model):
    name = TextField()
    description = TextField()
    owner_id = IntegerField()
    is_public = BooleanField()
    sg_rules = ArrayField() # ALTER TABLE public.scenarios ADD sg_rules TEXT[] DEFAULT array[]::TEXT[];
    topo = JsonBField()

    class Meta:
        table = 'scenarios'


class Lab(Model):
    name = TextField()
    description = TextField()
    owner_id = IntegerField()
    scenario_id = IntegerField()
    status = EnumField()
    preassessment_id = IntegerField()
    postassessment_id = IntegerField()
    allowed_attempts = ArrayField()

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


# Models for Assessment Module

class Assessment(Model):
    atitle = TextField()
    adescription = TextField()
    questions = ArrayField()
    scores = ArrayField()

    class Meta:
        table = 'assessments'

class Question(Model):
    qkind = TextField()
    qtitle = TextField()
    qtext = TextField()
    answers = ArrayField()
    correct = ArrayField()
    feedback = TextField()

    class Meta:
        table = 'questions'

class Report(Model):
    student = TextField()
    labname = TextField()
    assessmentid = TextField()
    answers = ArrayField()
    starttime = IntegerField()
    endtime = IntegerField()
    pre_post = IntegerField()
    attempt_num = IntegerField()

    class Meta:
        table = 'reports'

class Grade(Model):
    student = TextField()
    reportid = IntegerField()
    points = ArrayField()
    feedback = ArrayField()
    needsgrading = TextField()

    class Meta:
        table = 'grades'