from redis_db.managers import *

def test():
    PlayerManager.check_for_inactive_players()
