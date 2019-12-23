from rest_framework.authtoken.models import Token


def getUser(request):
    tok = request.headers.get('Authorization')
    return Token.objects.get(key=tok[6:len(tok)]).user
