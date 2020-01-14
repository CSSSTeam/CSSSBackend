from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User,Group


def getUser(request):
    tok = request.headers.get('Authorization')
    return Token.objects.get(key=tok[6:len(tok)]).user


def userList():
    return User.objects.all()


def userListInGroup(groupName):

    group = Group.objects.get(name=groupName)

    return group.user_set.all()
