from rest_framework.views import APIView
from rest_framework.response import Response
from users.permission import canOperatingInfo
from users.utility import getUser, deleteToken
from rest_framework import status


class detailsUser(APIView):
    permission_classes = [canOperatingInfo]

    def get(self, request):
        user = getUser(request)
        print(user)
        content = {
            'firstName': user.first_name,
            'lastName': user.last_name,
            'email': user.email,
            'groups': self.getGroups(user)
        }
        return Response(content)

    def getGroups(self, user):
        l = []
        for g in user.groups.all():
            l.append(g.name)
        return l

class logout(APIView):
    def post(self, request):
        deleteToken(request)
        return Response(status=status.HTTP_200_OK)