from postgrespy.models import Model
from postgrespy.fields import TextField, BooleanField


class User(Model):
    email = TextField()
    fullname = TextField()
    hash = TextField()
    is_root = BooleanField()

    class Meta:
        table = 'users'
