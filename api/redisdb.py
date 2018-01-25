import redis
import os

redis_token_db = redis.StrictRedis(host=os.environ['REDIS_HOST'],
                                   port=os.environ['REDIS_PORT'], db=os.environ['REDIS_TOKEN_DB'])
