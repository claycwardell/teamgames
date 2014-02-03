import pdb
from django.http import HttpResponse
from django.utils import simplejson as json
import functools
import chat.views


def jsonify(func):
    @functools.wraps(func)
    def wrap(request, *args, **kwargs):
        json_mime = 'application/json'
        if request.method == 'POST':
            request.POST = json.loads(request.body)
        ret = func(request, *args, **kwargs)
        return HttpResponse(json.dumps(ret), mimetype=json_mime)
    return wrap



def require_username(func):
    @functools.wraps(func)
    def wrap(request, *args, **kwargs):
        if not request.username:
            return chat.views.home(request)
        return func(request, *args, **kwargs)
    return wrap
