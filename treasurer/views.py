from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from treasurer.models import List, Member
from treasurer.permission import treasurerPerm
from treasurer.serializers import listSerializer, memberSerializer
from users.models import User

# ----------------------------LIST--------------------------------

class vList(APIView):
    permission_classes = [treasurerPerm]

    def post(self, request, id):
        try:
            lists = List.objects.get(id=id)
        except List.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404, status=status.HTTP_404_NOT_FOUND)

        serializer = listSerializer(lists,data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            lists = List.objects.get(id=id)
        except List.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404, status=status.HTTP_404_NOT_FOUND)

        lists.delete()
        return Response(settings.ERROR_MESSAGE_204, status=status.HTTP_204_NO_CONTENT)

class AllList(APIView):
    permission_classes = [treasurerPerm]

    def get(self, request):
        try:
            lists = List.objects.all()
        except List.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404, status=status.HTTP_404_NOT_FOUND)

        serializer = listSerializer(lists, context={'request': request}, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = listSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ----------------------------MEMBER--------------------------------

class vMember(APIView):
    permission_classes = [treasurerPerm]

    def post(self, request, id):

        try:
            members = Member.objects.get(id=id)
        except Member.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404, status=status.HTTP_404_NOT_FOUND)

        serializer = memberSerializer(members,data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):

        try:
            members = Member.objects.get(id=id)
        except Member.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404, status=status.HTTP_404_NOT_FOUND)

        members.delete()
        return Response(settings.ERROR_MESSAGE_204, status=status.HTTP_204_NO_CONTENT)

class AllMember(APIView):
    permission_classes = [treasurerPerm]

    def get(self, request):
        try:
            l = request.GET['list']

            members = Member.objects.filter(treasurerList = l)
        except List.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404, status=status.HTTP_404_NOT_FOUND)
        except MultiValueDictKeyError:
            return Response(settings.ERROR_MESSAGE_400, status=status.HTTP_400_BAD_REQUEST)

        serializer = memberSerializer(members, context={'request': request}, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = memberSerializer(data=request.data, context={'request': request}, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            id = int(request.GET['list'])

            users = User.objects.all()
            lists = List.objects.get(id=id)
        except (User.DoesNotExist, List.DoesNotExist):
            return Response(settings.ERROR_MESSAGE_404, status=status.HTTP_404_NOT_FOUND)
        except (ValueError, MultiValueDictKeyError):
            return Response(settings.ERROR_MESSAGE_400, status=status.HTTP_400_BAD_REQUEST)

        for u in users :
            member = Member.objects.get_or_create(user=u,treasurerList=lists)[0]
            member.save()

        return Response(settings.ERROR_MESSAGE_201, status=status.HTTP_201_CREATED)

class MemberByUser(APIView):
    permission_classes = [treasurerPerm]

    def get(self, request):
        try:
            u = request.GET['user']

            members = Member.objects.filter(user = u)
        except List.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404, status=status.HTTP_404_NOT_FOUND)
        except MultiValueDictKeyError:
            return Response(settings.ERROR_MESSAGE_400, status=status.HTTP_400_BAD_REQUEST)

        serializer = memberSerializer(members, context={'request': request}, many=True)
        return Response(serializer.data)

class MemberByIsPay(APIView):
    permission_classes = [treasurerPerm]

    def get(self, request):
        l = request.GET.get('list')
        u = request.GET.get('user')

        try:
            i = request.GET['isPay']

            if(l is None):
                if(u is None):
                    members = Member.objects.filter(isPay = i)
                else:
                    members = Member.objects.filter(isPay = i, user=u)
            else:
                if(u is None):
                    members = Member.objects.filter(isPay = i, treasurerList = l)
                else:
                    members = Member.objects.filter(isPay = i, user=u, treasurerList = l)
        except List.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404, status=status.HTTP_404_NOT_FOUND)
        except MultiValueDictKeyError:
            return Response(settings.ERROR_MESSAGE_400, status=status.HTTP_400_BAD_REQUEST)

        serializer = memberSerializer(members, context={'request': request}, many=True)
        return Response(serializer.data)
