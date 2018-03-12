import os
from rq import Queue
from redis import Redis

redis_conn = Redis(
    host=os.environ['REDIS_HOST'],
    port=os.environ['REDIS_PORT'],
    db=os.environ['REDIS_JOBS_DB'])

queue = Queue(connection=redis_conn)


