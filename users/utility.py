from rest_framework.authtoken.models import Token

def getUserObject(request):
    tok = request.headers.get('Authorization')
    if tok is None:
        return None
    try:
        user_object = Token.objects.get(key=tok.split(' ',1)[-1])
    except Token.DoesNotExist:
        return None
    return user_object

def getUser(request):
    user_object = getUserObject(request)
    if user_object:
        return user_object.user
    return None


def deleteToken(request):
    user_object = getUserObject(request)
    if user_object:
        getUserObject(request).delete()


def userHasPerm(request, permission):
    user = getUser(request)

    if user is None:
        return False
    if user.has_perm(permission):
        return True
    return False

