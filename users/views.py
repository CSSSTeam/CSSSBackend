from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


class detailsUser(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        user = Token.objects.get(key=request.headers.get('Authentication'))
        content = {
            'groups': user.created
        }
        return Response(content)
