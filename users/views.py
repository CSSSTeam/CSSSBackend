from rest_framework.views import APIView
from rest_framework.response import Response
from users.permission import canOperatingInfo
from users.utility import getUser


class detailsUser(APIView):
    permission_classes = [canOperatingInfo]

    def get(self, request):
        user = getUser(request)
        content = {
            'FirstName': user.first_name,
            'LastName': user.last_name,
            'Email': user.email,
        }
        return Response(content)

    def post(selfself, request):
        return Response(request.headers)
