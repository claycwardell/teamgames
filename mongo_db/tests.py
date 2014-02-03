import unittest
from managers import UserManager
from models import User
from teamgames_site import settings, consts
import random
import datetime
import pdb




class UserManagerTest(unittest.TestCase):
    def setUp(self):
        self.start_dt = datetime.datetime.now()
        self.test_user_list = []
        for i in xrange(100):
            random_delta = datetime.timedelta(seconds=random.randrange(1000))
            random_dt = self.start_dt - random_delta
            user = User(team=random.choice(consts.TEAM_CHOICES), username=str(i), last_ping=random_dt)
            user.save()
            self.test_user_list.append(user)
        for team in consts.TEAM_CHOICES:
            UserManager.assign_player(team)


    def test_assign_player(self):
        for team in consts.TEAM_CHOICES:
            player = User.objects.filter(is_player=True, team=team).get()
            idle_cutoff = self.start_dt - datetime.timedelta(settings.PLAYER_MAX_IDLE_SECONDS)
            self.assertGreater(player.last_ping, idle_cutoff)

    def test_get_player(self):
        for team in consts.TEAM_CHOICES:
            player = UserManager.get_player(team)
            self.assertEqual(player.is_player, True)

    def player_is_valid(self):
        for team in consts.TEAM_CHOICES:
            self.assertEqual(UserManager.check_if_player_is_valid(team))

    def tearDown(self):
        for user in self.test_user_list:
            user.delete()


suite = unittest.TestLoader().loadTestsFromTestCase(UserManagerTest)
unittest.TextTestRunner(verbosity=2).run(suite)