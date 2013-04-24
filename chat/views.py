from teamgames_site.consts import FIRST_CUTOFF, SECOND_CUTOFF, THIRD_CUTOFF, CUTOFF_TO_TEAM_MAP, SESSION_TEAM_KEY, SESSION_USERNAME_KEY
from teamgames_site.settings import PUSHER_APP_ID, PUSHER_KEY, PUSHER_SECRET
import pdb
from django.shortcuts import render_to_response
from decorators import jsonify, require_username
import logging

import pusher
from redis_db.managers import UsernameManager

pusher_instance = pusher.Pusher(app_id=PUSHER_APP_ID, key=PUSHER_KEY, secret=PUSHER_SECRET)

LOGGER = logging.getLogger(__name__)


#@require_GET
from django.views.decorators.csrf import csrf_exempt

def home(request):
    team = request.session.get("team")
    username = request.session.get("username")
    ctx = {
        'team' : team,
        'username' : username
    }
    return render_to_response('home.html', ctx)


#@require_POST
@csrf_exempt
@jsonify
def set_username(request):
    username = request.POST.get("username")
    team = request.session.get(SESSION_TEAM_KEY)
    print "username: %s" % username
    # check if available once redis is up
    redis_key = _get_username_team_key(username, team)
    available = not UsernameManager.get(redis_key)
    if available:
        request.session[SESSION_USERNAME_KEY] = username
        UsernameManager.set(username)

        return {'success' : True}
    return {'success' : False}

@jsonify
@csrf_exempt
@require_username
def new_message(request):
    message = request.POST.get("message")
    print "message: %s" % message
    username = request.session.get(SESSION_USERNAME_KEY)
    if message is not None:
        team = request.session.get(SESSION_USERNAME_KEY)
        pusher_instance[team].trigger('new-message', {"message" : message, "sender" : username, "player" : False})
        return {"success" : True}
    return {"success" : False}



def _get_username_team_key(username, team):
    return "%s-%s" % (username, team)











