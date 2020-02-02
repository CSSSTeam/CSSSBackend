from rest_framework.authtoken.models import Token


def getUser(request):
    tok = request.headers.get('Authorization')
    if tok is None:
        return None
    return Token.objects.get(key=tok[6:len(tok)]).user


def userHasPerm(request, permission):
    user = getUser(request)
    if user is None:
        return False
    if user.has_perm(permission):
        return True
    return False
