import logging
import random
from models import User
import datetime
from mongoengine.queryset import DoesNotExist, MultipleObjectsReturned
from teamgames_site import settings, consts
import pdb
from django_rq import job

LOGGER = logging.getLogger("%s.%s" % (settings.ROOT_LOGGER_NAME, __name__))

class UserManager(object):

    @classmethod
    def test_logging(cls):
        LOGGER.debug("Debug level message")
        LOGGER.info("Info level message")
        LOGGER.warning("Warning level message")
        LOGGER.error("Error level message")
        LOGGER.critical("Critical level message")


    @classmethod
    def get_user(cls, username):
        return User.objects.with_id(username)

    @classmethod
    def create_new_user(cls, username, team):
        ret = None
        pre_existing_user = cls.get_user(username)
        if pre_existing_user is None:
            new_user = User(
                username=username,
                team=team
            )
            ret = new_user.save()
        return ret

    @classmethod
    def receive_ping(cls, username):
        user = cls.get_user(username)
        LOGGER.debug("Pinging user %s", username)
        return user.update(set__last_ping=datetime.datetime.now())

    @classmethod
    def check_if_player_is_valid(cls, team):
        player_is_valid = False
        player = cls.get_player(team)
        if player is not None:
            if player.idle_seconds <= settings.PLAYER_MAX_IDLE_SECONDS:
                player_is_valid = True
        return player_is_valid

    @classmethod
    def get_player(cls, team):
        player = None
        try:
            player = User.objects.filter(team=team, is_player=True).get()

        except DoesNotExist:
            LOGGER.error("No player found on team %s", team)

        except MultipleObjectsReturned:
            LOGGER.error("Multiple players found for team %s", team)

        return player

    @classmethod
    def check_and_fix_all_players(cls):
        for team in consts.TEAM_CHOICES:
            if not cls.check_if_player_is_valid(team):
                cls.assign_player(team)

    @classmethod
    def assign_player(cls, team):
        LOGGER.debug("Assigning player to team %s", team)
        User.objects.filter(team=team, is_player=True).update(set__is_player=False, set__moves_since_player=0)
        right_now = datetime.datetime.now()
        cutoff_ping = right_now - datetime.timedelta(seconds=settings.PLAYER_MAX_IDLE_SECONDS)
        # If possible, pick an eligible player
        eligible_players = User.objects.filter(team=team, last_ping__gte=cutoff_ping)
        if eligible_players:
            new_player = random.choice(eligible_players)
        else:
            # If there isn't one, just give it to whoever pinged most recently
            new_player = User.objects.filter(team=team).order_by('-last_ping')[0]

        return new_player.update(set__is_player=True, set__moves_since_player=0)




@job("ping_users")
def receive_ping_async(username):
    UserManager.receive_ping(username)
