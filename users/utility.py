from rest_framework.authtoken.models import Token


def getUser(request):
    tok = request.headers.get('Authorization')
    if tok is None:
        return None
    try:
        user_object = Token.objects.get(key=tok[6:len(tok)])
    except Token.DoesNotExist:
        return None
    if user_object is None:
        return None
    return user_object.user


def deleteToken(request):
    tok = request.headers.get('Authorization')
    if tok is None:
        return
    try:
        user_object = Token.objects.get(key=tok[6:len(tok)])
    except Token.DoesNotExist:
        return 
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
