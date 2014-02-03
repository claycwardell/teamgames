from common_env import *


DOCUMENT_DATABASE = {
    "HOST" : "localhost",
    "NAME" : "teamgames_db"
}

REDIS_HOST = 'localhost'
REDIS_PORT = 6380

#REDIS_URL = "redis://%s:%s" % (REDIS_HOST, str(REDIS_PORT))

LOGGER.setLevel('DEBUG')


RQ_QUEUES = {}

for q in RQ_QUEUE_LIST:
    RQ_QUEUES[q] = {
        'HOST' : REDIS_HOST,
        'PORT' : REDIS_PORT,
        'DB' : RQ_REDIS_DB
    }
