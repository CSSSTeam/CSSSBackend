from rest_framework.views import APIView
from rest_framework.response import Response
from users.permission import canOperatingInfo
from users.utility import getUser


class detailsUser(APIView):
    permission_classes = [canOperatingInfo]

    def get(self, request):
        user = getUser(request)
        print(request.headers)
        content = {
            'FirstName': user.first_name,
            'LastName': user.last_name,
            'Email': user.email,
            'Groups': self.getGroups(user)
        }
        return Response(content)
    def getGroups(self,user):
        l=[]
        for g in user.groups.all():
            l.append(g.name)
        return l

