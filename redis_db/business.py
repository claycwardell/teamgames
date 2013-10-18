import pdb
import datetime
from redis_db.exceptions import AlreadyExistsException, NotFoundException
from redis_db.models import User, Team

class UserManager(object):

    @classmethod
    def create_new_user(cls, username, team_color=None):
        user = cls.get_user(username)
        if user is None:
            user = User(username=username)
            user.save()
            if team_color:
                team_obj = TeamManager.get_team(team_color, exception_on_not_found=False)
                if team_obj is None:
                    team_obj = TeamManager.create_team(team_color)
                cls.add_to_team(user.username, team_obj.color)
        else:
            raise AlreadyExistsException

        return user


    @classmethod
    def ping_user(cls, username):
        user = cls.get_user(username, exception_on_not_found=True)
        user.last_ping = datetime.datetime.now()
        return user.save()


    @classmethod
    def get_user(cls, username, exception_on_not_found=False):
        user = User.objects().get(username)
        if user is None and exception_on_not_found:
            raise NotFoundException
        return user




    @classmethod
    def add_to_team(cls, username, team_color):
        will_be_player = False
        team = TeamManager.get_team(team_color, exception_on_not_found=True)
        user = cls.get_user(username, exception_on_not_found=True)
        if not team.username_set:
            # First user on a team is automatically the player
            will_be_player = True
        team.username_set.add(user.username)
        user.team = team.color
        team.save()
        user.save()
        if will_be_player:
            TeamManager.set_player(user.username, team.color)


class TeamManager(object):

    @classmethod
    def get_team(cls, team_color, exception_on_not_found=False):
        team = Team.objects().get(team_color)
        if team is None and exception_on_not_found:
            raise NotFoundException
        return team

    @classmethod
    def create_team(cls, team_color):
        team = cls.get_team(team_color)
        if team is not None:
            raise AlreadyExistsException
        team = Team(color=team_color)
        return team.save()

    @classmethod
    def set_player(cls, username, team_color):
        user = UserManager.get_user(username, exception_on_not_found=True)
        team = cls.get_team(team_color, exception_on_not_found=True)
        if user.username not in team.username_set:
            raise ValueError("Trying to set a player on a team that he isn't on. username=%s team_color=%s" % (user.username, team.team_color))
        user.is_player = True
        user.save()
        team.player = user.username
        team.save()
