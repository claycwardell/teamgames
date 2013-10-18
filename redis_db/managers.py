import datetime
from datetime import timedelta
import pdb
import redis
from teamgames_site.settings import REDIS_HOST, REDIS_PORT, REDIS_DB
import pickle



class RedisDbClient(object):

    def __init__(self, redis_host=REDIS_HOST, redis_port=REDIS_PORT, redis_db=REDIS_DB):
        self._redis_host = redis_host
        self._redis_port = redis_port
        self._redis_db = redis_db
        self._pool = None
        self._redis_client = None


    @property
    def redis_client(self):
        if self._redis_client is None:
            self._redis_client = redis.Redis(connection_pool=self.pool)
        return self._redis_client

    @property
    def pool(self):
        if self._pool is None:
            self._pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        return self._pool


    def get(self, key):
        pickled = self.redis_client.get(key)
        if pickled is None:
            unpickled = None
        else:
            unpickled = pickle.loads(pickled)
        return unpickled


    def delete(self, key):
        return self.redis_client.delete(key)


    def set(self, key, obj):
        pickled = pickle.dumps(obj, -1)
        return self.redis_client.set(key, pickled)


    def keys(self):
        return self.redis_client.keys("*")


    def clear_all(self):
        keys = self.keys()
        if keys:
            return self.redis_client.delete(*keys)
        return "Db already emtpy"


    @staticmethod
    def get_compound_key(key1, key2):
        return "%s-%s", (key1, key2)


#class UsernameManager(RedisDbClient):
#    _prefix = RedisDbClient._prefix + "un:"
#
#    @classmethod
#    def initial_set(cls, username):
#        return super(UsernameManager, cls).set(username, cls.get_default_user_object(username))
#
#    @classmethod
#    def get_default_user_object(cls, username):
#        return {'last_ping' : None, 'username' : username, 'team' : None}


#    @classmethod
#    def update_ping(cls, username):
#        now = datetime.datetime.now()
#        player_dict = cls.get(username)
#        if player_dict is None:
#            raise ValueError("User doesn't exist")
#        player_dict['last_ping'] = now
#        cls.set(username, player_dict)


#class TeamManager(RedisDbClient):
#    _prefix = RedisDbClient._prefix + "tm:"
#
#    @classmethod
#    def add_to_team(cls, username, team):
#        RACE CONDITIONS ALERT
#        first_member = False
#        current_team = cls.get(team)
#        if current_team is None:
#            current_team = set()
#            first_member = True
#        current_team.add(username)
#        user_dict = UsernameManager.get(username)
#        user_dict['team'] = team
#        UsernameManager.set(username, user_dict)
#        if first_member:
#            PlayerManager.make_player(username)
#        return cls.set(team, current_team)
#
#
#class PlayerManager(RedisDbClient):
#    _prefix = RedisDbClient._prefix + "pl"
#    _teams = ['green', 'red', 'blue']
#    _inactive_period = timedelta(seconds=90)
#
#    @classmethod
#    def set(cls, team, username):
#        cls.unassign_player(team)
#        user_dict = UsernameManager.get(username)
#        if user_dict is not None:
#            PlayerManager.set(user_dict['username'], user_dict)
#            return super(PlayerManager, cls).set(team, username)
#
#
#    @classmethod
#    def get(cls, team):
#        username = super(PlayerManager, cls).get(team)
#        user = UsernameManager.get(username)
#        return user
#
#    @classmethod
#    def get_all_players(cls):
#        result_dict = {}
#        for team in cls._teams:
#            result_dict[team] = cls.get(team)
#        return result_dict
#
#    @classmethod
#    def check_for_inactive_players(cls):
#        now = datetime.datetime.now()
#        player_map = cls.get_all_players()
#        for team in player_map:
#            player = player_map[team]
#            if player is None or (now - player['last_ping']) > cls._inactive_period:
#                    cls.reassign_player_for_team(team)
#
#
#    @classmethod
#    def reassign_player_for_team(cls, team):
#        usernames = TeamManager.get(team)
#        if usernames is not None:
#            for u in usernames:
#                user = UsernameManager.get(u)
#                if cls.get_inactive_period(user) < cls._inactive_period:
#                    cls.make_player(user['username'])
#
#    @classmethod
#    def make_player(cls, username):
#        username_dict = UsernameManager.get(username)
#        cls.set(username_dict['team'], username_dict['username'])
#        PlayerManager.set(username, username_dict)
#
#    @classmethod
#    def unassign_player(cls, team):
#        player = cls.get(team)
#        if player is not None:
#            UsernameManager.set(player['username'], player)
#
#    @staticmethod
#    def get_inactive_period(user):
#        now = datetime.datetime.now()
#        return now - user['last_ping']
#
#
#
#
#