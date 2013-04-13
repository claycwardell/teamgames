import redis
from teamgames_site.settings import REDIS_URL


redis_client = redis.from_url(REDIS_URL, db=0)


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
    def set(cls, id, obj):
        key = cls._get_key(id)
        return redis_client.set(key, obj)




class UsernameManager(RedisDbManager):
    _prefix = super(RedisDbManager, self)._prefix + "username:"
