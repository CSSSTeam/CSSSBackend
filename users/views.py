import json

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework.response import Response
from users.permission import canOperatingInfo, canAdministionOnCurrent
from users.utility import getUser, deleteToken
from rest_framework import status


class currentUserAdmin(APIView):
    permission_classes = [canAdministionOnCurrent]

    def get(self, request, pk):
        user = User.objects.get(id=pk)
        content = getDetail(user)
        return Response(content)

    def delete(self, request, pk):
        User.objects.get(id=pk).delete()
        return Response(status=status.HTTP_200_OK)


def checkData(newUser):
    return True


class AdministrationUser(APIView):
    def get(self, request):
        users = User.objects.all()
        content = []
        for user in users:
            content.append({
                'id': user.id,
                'username': user.username,
                'firstName': user.first_name,
                'lastName': user.last_name
            })
        return Response(content)

    def post(self, request):
        newUser = json.loads(request.body)
        if not checkData(newUser):
            return Response("Your data is invalid", status=status.HTTP_400_BAD_REQUEST)
        print(newUser)
        groups = []
        try:
            for gr in newUser['groups']:
                group = Group.objects.get(id=gr)
                groups.append(group)
        except Exception as exception:
            if exception == "not Found":
                return Response("Group is not found", status=status.HTTP_404_NOT_FOUND)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create(username=newUser['username'], first_name=newUser['firstName'],
                                   last_name=newUser['lastName'], email=newUser['email'],
                                   password=make_password(newUser['password']))
        for group in groups:
            user.groups.add(group)
        user.save()
        return Response(status=status.HTTP_201_CREATED)


def getGroups(user):
    l = []
    for g in user.groups.all():
        l.append(g.name)
    return l


def getDetail(user):
    content = {
        'id': user.id,
        'username': user.username,
        'firstName': user.first_name,
        'lastName': user.last_name,
        'email': user.email,
        'groups': getGroups(user)
    }
    return content


class detailsUser(APIView):
    permission_classes = [canOperatingInfo]

    def get(self, request):
        user = getUser(request)
        content = getDetail(user)
        return Response(content)


class logout(APIView):
    def post(self, request):
        deleteToken(request)
        return Response(status=status.HTTP_200_OK)
