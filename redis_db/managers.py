import redis
from teamgames_site.settings import REDIS_HOST, REDIS_PORT, REDIS_DB

pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
redis_client = redis.Redis(connection_pool=pool)


class RedisDbManager(object):
    _prefix = "db:"

    @classmethod
    def _get_key(cls, id):
        return "%s%s" % (cls._prefix, id)

    @classmethod
    def get(cls, id):
        key = cls._get_key(id)
        return redis_client.get(key)

    @classmethod
    def delete(cls, id):
        key = cls._get_key(id)
        return redis_client.delete(key)

    @classmethod
    def set(cls, id, obj):
        key = cls._get_key(id)
        return redis_client.set(key, obj)




class UsernameManager(RedisDbManager):
    _prefix = RedisDbManager._prefix + "un:"

