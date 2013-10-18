import datetime
from redis_db.business import UserManager
from redis_db.exceptions import AlreadyExistsException
from teamgames_site.consts import FIRST_CUTOFF, SECOND_CUTOFF, THIRD_CUTOFF, CUTOFF_TO_TEAM_MAP, SESSION_TEAM_KEY, SESSION_USERNAME_KEY
from teamgames_site.settings import PUSHER_APP_ID, PUSHER_KEY, PUSHER_SECRET
import pdb
from django.shortcuts import render_to_response
from decorators import jsonify, require_username
import logging

import pusher

pusher_instance = pusher.Pusher(app_id=PUSHER_APP_ID, key=PUSHER_KEY, secret=PUSHER_SECRET)

logging.basicConfig(level='DEBUG')


#@require_GET
from django.views.decorators.csrf import csrf_exempt

@jsonify
def home(request):
    team = request.session.get("team")
    username = request.session.get("username")

    if username:
        try:
            UserManager.create_new_user(username, team)
        except AlreadyExistsException:
            logging.info("User with username: %s already exists, not creating", username)

    ctx = {
        'team' : team,
        'username' : username
    }
    return ctx


#@require_POST
@csrf_exempt
@jsonify
def set_username(request):
    username = request.POST.get("username")
    team = request.session.get(SESSION_TEAM_KEY)
    logging.info("username: %s", username)
    try:
        UserManager.create_new_user(username, team)
        return {'success' : True}
    except AlreadyExistsException:
        return {'success' : False}

@jsonify
@csrf_exempt
@require_username
def new_message(request):
    message = request.POST.get("message")
    logging.info("message: %s" % message)
    user = request.session_user
    if message is not None:
        team = request.session.get(SESSION_TEAM_KEY)
        pusher_instance[team].trigger('new-message', {"message" : message, "sender" : user.username, "player" : user.is_player})
        return {"success" : True}
    return {"success" : False}


@jsonify
@csrf_exempt
@require_username
def receive_ping(request):
    now = datetime.datetime.now()
    user_dict = request.session_user
    user_dict['last_ping'] = now
    UsernameManager.set(user_dict['username'], user_dict)
    return {"success" : True}




def _get_username_team_key(username, team):
    return "%s-%s" % (username, team)











