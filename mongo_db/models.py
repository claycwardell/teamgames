import mongoengine
from teamgames_site import consts
import datetime


class User(mongoengine.Document):
    meta = {'allow_inheritance' : True}
    username = mongoengine.StringField(primary_key=True)
    team = mongoengine.StringField(choices=consts.TEAM_CHOICES, required=True)
    is_player = mongoengine.BooleanField(default=False)
    last_ping = mongoengine.DateTimeField(default=datetime.datetime.now)
    moves_since_player = mongoengine.IntField(default=0)

    def idle_seconds(self):
        idle_delta = datetime.datetime.now() - self.last_ping
        idle_seconds = idle_delta.total_seconds()
        return idle_seconds

    def __unicode__(self):
        return self.username