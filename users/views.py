import json

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework.response import Response
from users.permission import canOperatingInfo, canAdministionOnCurrent, canAdministionUser
from users.serializers import UserSerializer, UserDisplaySerializer, UserCreator
from users.utility import getUser, deleteToken
from rest_framework import status


class currentUserAdmin(APIView):
    permission_classes = [canAdministionOnCurrent]

    def get(self, request, pk):
        user = User.objects.get(id=pk)
        userSerialized = UserDisplaySerializer(user)
        return Response(userSerialized.data)

    def delete(self, request, pk):
        User.objects.get(id=pk).delete()
        return Response(status=status.HTTP_200_OK)


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


# TODO(n2one): CREATE ADMINISTRATION ON GROUP


class detailsUser(APIView):
    permission_classes = [canOperatingInfo]

    def get(self, request):
        user = getUser(request)
        content = UserDisplaySerializer(user)
        return Response(content)


class logout(APIView):
    def post(self, request):
        deleteToken(request)
        return Response(status=status.HTTP_200_OK)
