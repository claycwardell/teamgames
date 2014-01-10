from mongo_db.models import User


class UserManager(object):

    @classmethod
    def create_new_user(cls, username, team):
        ret = None
        pre_existing_user = User.objects.with_id(username)
        if pre_existing_user is None:
            new_user = User(
                username=username,
                team=team
            )
            ret = new_user.save()
        return ret

