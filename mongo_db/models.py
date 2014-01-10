import mongoengine
from teamgames_site import consts
import datetime






class User(mongoengine.Document):
    username = mongoengine.StringField(primary_key=True)
    team = mongoengine.StringField(choices=consts.TEAM_CHOICES, required=True)
    is_player = mongoengine.BooleanField(default=False)
    last_ping = mongoengine.DateTimeField(default=datetime.datetime.now)
