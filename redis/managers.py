import redis
from teamgames_site.settings import REDIS_URL


redis_client = redis.from_url(REDIS_URL, db=0)


class RedisDbManager(object):
    _prefix = "db:"

    @classmethod
    def _get_key(cls, id):
        return "%s:%s" % (cls._prefix, id)

    @classmethod
    def get(cls, id):
        return redis_client.get(cls._get_key(id))

    @classmethod
    def set(cls):