from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User,Group


def getUser(request):
    tok = request.headers.get('Authorization')
    if tok is None:
        return None
    user_object = Token.objects.get(key=tok[6:len(tok)])
    if user_object is None:
        return None
    return user_object.user


def deleteToken(request):
    tok = request.headers.get('Authorization')
    if tok is None:
        return
    user_object = Token.objects.get(key=tok[6:len(tok)])
    if user_object is None:
        return
    user_object.delete()


def userHasPerm(request, permission):
    user = getUser(request)
    if user is None:
        return False
    if user.has_perm(permission):
        return True
    return False

def userList():
    return User.objects.all()


def userListInGroup(groupName):

    group = Group.objects.get(name=groupName)

    return group.user_set.all()
