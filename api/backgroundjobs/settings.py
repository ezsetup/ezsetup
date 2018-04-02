"""Settings for rq workers
Use `rq worker -c setttings` to run a rq worker with this setting"""

import os

REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = os.environ['REDIS_PORT']
REDIS_DB = os.environ['REDIS_JOBS_DB']

if os.environ.get('SENTRY_DSN') is not None:
    SENTRY_DSN = 'sync+' + os.environ['SENTRY_DSN']
