from django.utils.datastructures import MultiValueDictKeyError

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from treasurer.models import TreasurerList, Member
from treasurer.permission import canShow, canCreate
from treasurer.serializers import treasurerListSerializer, memberSerializer

#------------------------GET-------------------------
@api_view(['GET'])
@permission_classes([canShow])
def getAllLists(request, format=None):

    try:
        list = TreasurerList.objects.all()
    except TreasurerList.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = treasurerListSerializer(list, context={'request': request}, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([canShow])
def getAllMemberByLists(request, format=None):

    try:
        l = request.GET['list']

        members = Member.objects.filter(treasurerList = l)
    except TreasurerList.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except MultiValueDictKeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    serializer = memberSerializer(members, context={'request': request}, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([canShow])
def getAllMemberByUser(request, format=None):

    try:
        u = request.GET['user']

        members = Member.objects.filter(user = u)
    except TreasurerList.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except MultiValueDictKeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    serializer = memberSerializer(members, context={'request': request}, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([canShow])
def getAllMemberByIsPay(request, format=None):

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
    except TreasurerList.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except MultiValueDictKeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    serializer = memberSerializer(members, context={'request': request}, many=True)
    return Response(serializer.data)