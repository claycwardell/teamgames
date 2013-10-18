from business import UserManager
from redis_db.managers import RedisDbClient


def test():
    UserManager.create_new_user('Clay', 'green')


def clean():
    redis_client = RedisDbClient()
    redis_client.clear_all()