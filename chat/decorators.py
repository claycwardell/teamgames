from django.http import HttpResponse
from django.utils import simplejson as json
import functools






def jsonify(func):
    @functools.wraps
    def wrap(*args, **kwargs):
        json_mime = 'application/json'
        ret = func(*args, **kwargs)
        return HttpResponse(json.dumps(ret), mimetype=json_mime)
    return wrap