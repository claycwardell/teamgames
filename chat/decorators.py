import pdb
from django.http import HttpResponse
from django.utils import simplejson as json
import functools
import chat.views
from redis_db.business import UserManager
from teamgames_site.consts import SESSION_USERNAME_KEY


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
        username = request.session.get(SESSION_USERNAME_KEY)
        if not username:
            return chat.views.home(request)
        user = UserManager.get_user(username)
        if user is None:
            user = UserManager.create_new_user(username)

        request.session_user = user

        return func(request, *args, **kwargs)
    return wrap
