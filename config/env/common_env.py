import logging


REDIS_DB = 0
RQ_REDIS_DB = 1

ROOT_LOGGER_NAME = "teamgames_logger"

LOGGER = logging.getLogger(ROOT_LOGGER_NAME)


RQ_QUEUE_LIST = [
    'ping_users',
    'check_players'
]