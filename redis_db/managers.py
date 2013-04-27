import datetime
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
        if keys:
            return cls._redis_client.delete(*keys)
        return "Db already emtpy"



class UsernameManager(RedisDbManager):
    _prefix = RedisDbManager._prefix + "un:"

    @classmethod
    def initial_set(cls, username):
        return super(UsernameManager, cls).set(username, cls.get_default_user_object(username))

    @classmethod
    def make_player(cls, username):
        username_dict = cls.get(username)
        username_dict['player'] = True
        return cls.set(username, username_dict)

    @classmethod
    def get_default_user_object(cls, username):
        return {'player' : False, 'last_ping' : None, 'username' : username}

#    @classmethod
#    def update_ping(cls, username):
#        now = datetime.datetime.now()
#        player_dict = cls.get(username)
#        if player_dict is None:
#            raise ValueError("User doesn't exist")
#        player_dict['last_ping'] = now
#        cls.set(username, player_dict)





class TeamManager(RedisDbManager):
    _prefix = RedisDbManager._prefix + "tm:"

    @classmethod
    def add_to_team(cls, username, team):
        # RACE CONDITIONS ALERT
        first_member = False
        current_team = cls.get(team)
        if current_team is None:
            current_team = set()
            first_member = True
        current_team.add(username)
        if first_member:
            UsernameManager.make_player(username)
        return cls.set(team, current_team)


    @classmethod
    def check_for_player(cls, team):
        found = False
        if any([u['player'] for u in cls.get(team)]):
            found = True
        return found

