# -*- coding: utf-8 -*-
import hashlib
from teamgames_site.consts import FIRST_CUTOFF, SECOND_CUTOFF, THIRD_CUTOFF, CUTOFF_TO_TEAM_MAP



class MainMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.session.get('team'):
            request.session['team'] = self._get_team_from_ip(request.META['REMOTE_HOST'])
        return

    @staticmethod
    def _get_team_from_ip(ip):
        digest = hashlib.sha1(ip).hexdigest()
        digest_int = int(digest, 16)
        if FIRST_CUTOFF <= digest_int < SECOND_CUTOFF:
            team = CUTOFF_TO_TEAM_MAP[FIRST_CUTOFF]
        elif SECOND_CUTOFF <= digest_int < THIRD_CUTOFF:
            team = CUTOFF_TO_TEAM_MAP[SECOND_CUTOFF]
        elif THIRD_CUTOFF <= digest_int:
            team = CUTOFF_TO_TEAM_MAP[THIRD_CUTOFF]
        else:
            raise ValueError("Clusterfuck has ensued")
        return team