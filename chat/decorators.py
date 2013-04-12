import pdb
from django.http import HttpResponse
from django.utils import simplejson as json
import functools






def jsonify(func):
    @functools.wraps
    def wrap(request, *args, **kwargs):
        pdb.set_trace()
        json_mime = 'application/json'
        if request.method == 'POST':
            request.POST = json.loads(request.body)
        ret = func(request, *args, **kwargs)
        return HttpResponse(json.dumps(ret), mimetype=json_mime)
    return wrap