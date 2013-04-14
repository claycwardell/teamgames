import redis
from teamgames_site.settings import REDIS_HOST, REDIS_PORT, REDIS_DB
import cPickle



class RedisDbManager(object):
    _pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    _redis_client = redis.Redis(connection_pool=_pool)

    _prefix = "db:"

    @classmethod
    def _get_key(cls, id):
        return "%s%s" % (cls._prefix, id)

    @classmethod
    def get(cls, id):
        key = cls._get_key(id)
        pickled = cls._redis_client.get(key)
        if pickled is None:
            unpickled = None
        else:
            unpickled = cPickle.loads(pickled)
        return unpickled

    @classmethod
    def delete(cls, id):
        key = cls._get_key(id)
        return cls._redis_client.delete(key)

    @classmethod
    def set(cls, id, obj):
        key = cls._get_key(id)
        pickled = cPickle.dumps(obj)
        return cls._redis_client.set(key, pickled)

    @classmethod
    def keys(cls):
        return cls._redis_client.keys("%s*" % cls._prefix)

    @classmethod
    def clear_all(cls):
        keys = cls.keys()
        return cls._redis_client.delete(*keys)



class UsernameManager(RedisDbManager):
    _prefix = RedisDbManager._prefix + "un:"

    @classmethod
    def set(cls, username):
        return super(UsernameManager, cls).set(username, True)




class TeamManager(RedisDbManager):
    _prefix = RedisDbManager._prefix + "tm:"

    @classmethod
    def add_to_team(cls, username, team):
        # RACE CONDITIONS ALERT
        current_team = cls.get(team)
        if current_team is None:
            current_team = set()
        current_team.add(username)
        return cls.set(team, current_team)

