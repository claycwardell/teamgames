import datetime
from datetime import timedelta
import pdb
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


    @staticmethod
    def get_compound_key(key1, key2):
        return "%s-%s", (key1, key2)


class UsernameManager(RedisDbManager):
    _prefix = RedisDbManager._prefix + "un:"

    @classmethod
    def initial_set(cls, username):
        return super(UsernameManager, cls).set(username, cls.get_default_user_object(username))

    @classmethod
    def get_default_user_object(cls, username):
        return {'last_ping' : None, 'username' : username, 'team' : None}


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
        user_dict = UsernameManager.get(username)
        user_dict['team'] = team
        UsernameManager.set(username, user_dict)
        if first_member:
            PlayerManager.make_player(username)
        return cls.set(team, current_team)


class PlayerManager(RedisDbManager):
    _prefix = RedisDbManager._prefix + "pl"
    _teams = ['green', 'red', 'blue']
    _inactive_period = timedelta(seconds=90)

    @classmethod
    def set(cls, team, username):
        cls.unassign_player(team)
        user_dict = UsernameManager.get(username)
        if user_dict is not None:
            PlayerManager.set(user_dict['username'], user_dict)
            return super(PlayerManager, cls).set(team, username)


    @classmethod
    def get(cls, team):
        username = super(PlayerManager, cls).get(team)
        user = UsernameManager.get(username)
        return user

    @classmethod
    def get_all_players(cls):
        result_dict = {}
        for team in cls._teams:
            result_dict[team] = cls.get(team)
        return result_dict

    @classmethod
    def check_for_inactive_players(cls):
        now = datetime.datetime.now()
        player_map = cls.get_all_players()
        for team in player_map:
            player = player_map[team]
            if player is None or (now - player['last_ping']) > cls._inactive_period:
                    cls.reassign_player_for_team(team)


    @classmethod
    def reassign_player_for_team(cls, team):
        usernames = TeamManager.get(team)
        if usernames is not None:
            for u in usernames:
                user = UsernameManager.get(u)
                if cls.get_inactive_period(user) < cls._inactive_period:
                    cls.make_player(user['username'])

    @classmethod
    def make_player(cls, username):
        username_dict = UsernameManager.get(username)
        cls.set(username_dict['team'], username_dict['username'])
        PlayerManager.set(username, username_dict)

    @classmethod
    def unassign_player(cls, team):
        player = cls.get(team)
        if player is not None:
            UsernameManager.set(player['username'], player)

    @staticmethod
    def get_inactive_period(user):
        now = datetime.datetime.now()
        return now - user['last_ping']





