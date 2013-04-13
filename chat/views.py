from teamgames_site.consts import FIRST_CUTOFF, SECOND_CUTOFF, THIRD_CUTOFF, CUTOFF_TO_TEAM_MAP
from teamgames_site.settings import PUSHER_APP_ID, PUSHER_KEY, PUSHER_SECRET
import pdb
from django.shortcuts import render_to_response
from decorators import jsonify, require_username

import pusher

pusher_instance = pusher.Pusher(app_id=PUSHER_APP_ID, key=PUSHER_KEY, secret=PUSHER_SECRET)



#@require_GET
from django.views.decorators.csrf import csrf_exempt
from chat.decorators import jsonify

def home(request):
    team = request.session.get("team")
    ctx = {'team' : team}
    return render_to_response('home.html', ctx)


#@require_POST
@csrf_exempt
@jsonify
def set_username(request):
    username = request.POST.get("username")

    # check if available
    available = True
    if available:
        request.session['username'] = username
    return {'success' : True}

@jsonify
@csrf_exempt
@require_username
def new_message(request):
    message = request.POST.get("message")
    if message is not None:
        team = request.session.get("team")
        pusher_instance[team].trigger('new-message', {"message" : message})
        return {"success" : True}
    return {"success" : False}












