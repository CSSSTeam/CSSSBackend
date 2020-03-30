import json

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework.response import Response
from users.permission import canOperatingInfo, canAdministionOnCurrent, canAdministionUser
from users.serializers import UserSerializer, UserDisplaySerializer, UserCreator, GroupSerializer, \
    GroupDisplaySerializer, GroupCreator
from users.utility import getUser, deleteToken
from rest_framework import status


# ---------------------Users--------------------------
class currentUserAdmin(APIView):
    permission_classes = [canAdministionOnCurrent]

    def get(self, request, pk):
        user = User.objects.get(id=pk)
        userSerialized = UserDisplaySerializer(user)
        return Response(userSerialized.data)

    def delete(self, request, pk):
        User.objects.get(id=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class detailsUser(APIView):
    permission_classes = [canOperatingInfo]

    def get(self, request):
        user = getUser(request)
        content = UserDisplaySerializer(user)
        return Response(content.data)


class AdministrationUser(APIView):
    permission_classes = [canAdministionUser]

    def get(self, request):
        users = User.objects.all()

        userSerialized = UserSerializer(users, many=True)
        return Response(userSerialized.data)

    def post(self, request):
        newUser = UserCreator(data=request.data)
        try:
            newUser.is_valid(True)
        except Exception as e:
            return Response(newUser.errors, status=status.HTTP_400_BAD_REQUEST)

        newUser.save()
        return Response(status=status.HTTP_201_CREATED)


# -------------Groups-----------------------------

class currentGroupAdmin(APIView):
    permission_classes = [canAdministionOnCurrent]

    def get(self, request, pk):
        try:
            group = Group.objects.get(id=pk)
        except Exception as e:
            print(str(e))
        group_serialized = GroupDisplaySerializer(group)
        return Response(group_serialized.data)

    def delete(self, request, pk):
        try:
            Group.objects.get(id=pk).delete()
        except Exception as e:
            print(str(e))
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdministrationGroup(APIView):
    permission_classes = [canAdministionUser]

    def get(self, request):
        groups = Group.objects.all()

        groups_serialized = GroupSerializer(groups, many=True)
        return Response(groups_serialized.data)

    def post(self, request):
        newGroup = GroupCreator(data=request.data)
        try:
            newGroup.is_valid(True)
        except Exception as e:
            return Response(newGroup.errors, status=status.HTTP_400_BAD_REQUEST)

        newGroup.save()
        return Response(status=status.HTTP_201_CREATED)

#---------other---------------------------------------------------------
class logout(APIView):
    def post(self, request):
        deleteToken(request)
        return Response(status=status.HTTP_200_OK)
