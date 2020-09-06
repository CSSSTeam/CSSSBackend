import json

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, User
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from users.permission import (canAdministionOnCurrent, canAdministionUser,
                              canOperatingInfo)
from users.serializers import (ChangePasswordSerializer, GroupCreator,
                               GroupDisplaySerializer, GroupSerializer,
                               UserCreator, UserDisplaySerializer,
                               UserSerializer)
from users.utility import deleteToken, getUser


# ---------------------Users--------------------------
class currentUserAdmin(APIView):
    permission_classes = [canAdministionOnCurrent]

    def get(self, request, pk):
        user = User.objects.get(id=pk)
        userSerialized = UserDisplaySerializer(user)
        return Response(userSerialized.data)

    def delete(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            token = Token.objects.get(user=user)
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        token.delete()
        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class detailsUser(APIView):
    permission_classes = [canOperatingInfo]

    def get(self, request):
        user = getUser(request)
        content = UserDisplaySerializer(user)
        return Response(content.data)


class changePassword(APIView):
    permission_classes = [canOperatingInfo]

    def post(self, request):
        changePassword = ChangePasswordSerializer(data=request.data)
        try:
            changePassword.is_valid(True)
        except Exception as e:
            return Response(changePassword.errors, status=status.HTTP_400_BAD_REQUEST)
        user = getUser(request)

        if not user.check_password(changePassword.validated_data['oldPass']):
            return Response({"error": "Old Password not be correct"}, status=status.HTTP_401_UNAUTHORIZED)
        if not changePassword.validated_data['newPass'] == changePassword.validated_data['newPass2']:
            return Response({"error": "New Password is different"}, status=status.HTTP_417_EXPECTATION_FAILED)

        user.set_password(changePassword.validated_data['newPass'])
        user.save()
        return Response(status=status.HTTP_200_OK)


class AdministrationUser(APIView):
    permission_classes = [canAdministionUser]

    def get(self, request):
        users = User.objects.all()

        userSerialized = UserSerializer(users, many=True)
        return Response(userSerialized.data)

    def post(self, request):
        serializer = UserCreator(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AdministrationUserGroup(APIView):
    permission_classes = [canAdministionUser]

    def post(self, request):
        try:
            userId = request.GET['user']
            groupId = request.GET['group']

            group = Group.objects.get(pk=groupId)
            user = User.objects.get(pk=userId)

        except (User.DoesNotExist, Group.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
        except  MultiValueDictKeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        group.user_set.add(user)
        return Response(status=status.HTTP_200_OK)
    
    def delete(self, request):
        try:
            userId = request.GET['user']
            groupId = request.GET['group']

            group = Group.objects.get(pk=groupId)
            user = User.objects.get(pk=userId)

        except (User.DoesNotExist, Group.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
        except  MultiValueDictKeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        group.user_set.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

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


# ---------other---------------------------------------------------------
class logout(APIView):
    def post(self, request):
        deleteToken(request)
        return Response(status=status.HTTP_200_OK)
