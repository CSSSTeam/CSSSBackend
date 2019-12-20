from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


class detailsUser(APIView):
    def post(self, request):
        tok = request.headers.get('Authorization')
        print(tok[6:len(tok)+1])
        user = Token.objects.get(key=tok[6:len(tok)])
        content = {
            'FirstName': user.user.first_name,
            'LastName': user.user.last_name,
            'Email': user.user.email,
        }
        return Response(content)
