import datetime
from redis_db.exceptions import AlreadyExistsException
from teamgames_site.consts import FIRST_CUTOFF, SECOND_CUTOFF, THIRD_CUTOFF, CUTOFF_TO_TEAM_MAP, SESSION_TEAM_KEY, SESSION_USERNAME_KEY
from teamgames_site.settings import PUSHER_APP_ID, PUSHER_KEY, PUSHER_SECRET
import pdb
from django.shortcuts import render_to_response
from decorators import jsonify, require_username
import logging
from teamgames_site import settings

from mongo_db.managers import UserManager, receive_ping_async

import pusher

pusher_instance = pusher.Pusher(app_id=PUSHER_APP_ID, key=PUSHER_KEY, secret=PUSHER_SECRET)

LOGGER = logging.getLogger("%s.%s" % (settings.ROOT_LOGGER_NAME, __name__))


#@require_GET
from django.views.decorators.csrf import csrf_exempt

@jsonify
def home(request):
    team = request.session.get("team")
    username = request.session.get("username")

    #if username:
    #    try:
    #        UserManager.create_new_user(username, team)
    #    except AlreadyExistsException:
    #        logging.info("User with username: %s already exists, not creating", username)

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
    team = request.team
    LOGGER.info("Setting username: %s", username)
    try:
        UserManager.create_new_user(username, team)
        request.session[SESSION_USERNAME_KEY] = username
        return {'success' : True}
    except AlreadyExistsException:
        return {'success' : False}


@csrf_exempt
@require_username
@jsonify
def new_message(request):
    message = request.POST.get("message")
    logging.info("message: %s" % message)
    username = request.username
    user = UserManager.get_user(username)
    if message is not None and user is not None:
        team = request.team
        pusher_instance[team].trigger('new-message', {"message" : message, "sender" : user.username, "player" : user.is_player})
        return {"success" : True}
    return {"success" : False}


@jsonify
@csrf_exempt
@require_username
def receive_ping(request):
    RUN_ASYNC = True
    username = request.username
    if RUN_ASYNC:
        receive_ping_async.delay(username)
    else:
        receive_ping_async(username)
    return {"success" : True}










