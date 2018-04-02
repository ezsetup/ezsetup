import os
from manage import create_root

create_root(os.environ['EZSETUP_ROOT_EMAIL'], os.environ['EZSETUP_ROOT_PASSWORD'], os.environ['EZSETUP_ROOT_USER'])

