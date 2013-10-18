from copy import copy
from redis_db.managers import RedisDbClient

class ObjectManager(object):
    def __init__(self, model_class):
        self._model_class = model_class
        self._redis_client = None

    @property
    def model_class(self):
        return self._model_class

    @property
    def redis_client(self):
        if self._redis_client is None:
            self._redis_client = RedisDbClient()
        return self._redis_client

    def get(self, id):
        return self.redis_client.get(self.get_key(id))

    def get_key(self, id):
        return self.model_class.model_prefix + id


class RedisDocument(object):
    prefix = "db:"
    _objects = None

    def __init__(self):
        self._redis_client = None

    def save(self):
        the_copy = copy(self)
        the_copy._clean_for_set()
        self.redis_client.set(the_copy.get_key(), the_copy)
        return self

    def get_key(self):
        return self.prefix + self.id

    def _clean_for_set(self):
        self._redis_client = None

    @property
    def redis_client(self):
        if self._redis_client is None:
            self._redis_client = RedisDbClient()
        return self._redis_client

    @classmethod
    def objects(cls):
        if type(cls) == RedisDocument:
            raise NotImplementedError
        if cls._objects is None:
            cls._objects = ObjectManager(cls)
        return cls._objects



class User(RedisDocument):
    """
    Basic User object
    """

    model_prefix = RedisDocument.prefix + "usr:"


    def __init__(self, username):
        self.id = username     # The users chosen username
        self.team = None        # The users team (as a string, the color)
        self.is_player = False  # Is Player
        self.last_ping = None   # Last successful ping from the users browser
        super(User, self).__init__()


    @property
    def prefix(self):
        return User.model_prefix

    @property
    def username(self):
        return self.id



class Team(RedisDocument):
    model_prefix = "tm:"

    def __init__(self, color, player=None):
        self.id = color
        self.player = player
        self.username_set = set()
        super(Team, self).__init__()


    @property
    def prefix(self):
        return Team.model_prefix

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, player):
        self._player = player

    @property
    def color(self):
        return self.id