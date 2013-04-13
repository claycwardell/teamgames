import hashlib
from teamgames_site.consts import FIRST_CUTOFF, SECOND_CUTOFF, THIRD_CUTOFF, CUTOFF_TO_TEAM_MAP
import pdb
import json
from django.utils import simplejson
from django.http import HttpResponse
from django.shortcuts import render_to_response





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
    pdb.set_trace()
    username = request.POST.get("username")

    # check if available
    available = True
    if available:
        request.session['username'] = username
    return {'success' : True}

@csrf_exempt
@jsonify
def new_message(request):
    pass










