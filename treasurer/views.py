from django.utils.datastructures import MultiValueDictKeyError

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from treasurer.models import List, Member
from treasurer.permission import canShow, canCreate
from treasurer.serializers import listSerializer, memberSerializer


#------------------------GET-------------------------
@api_view(['GET'])
@permission_classes([canShow])
def getAllLists(request):

    try:
        lists = List.objects.all()
    except List.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = listSerializer(lists, context={'request': request}, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([canShow])
def getAllMemberByLists(request):

    try:
        l = request.GET['list']

        members = Member.objects.filter(treasurerList = l)
    except List.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except MultiValueDictKeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    serializer = memberSerializer(members, context={'request': request}, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([canShow])
def getAllMemberByUser(request):

    try:
        u = request.GET['user']

        members = Member.objects.filter(user = u)
    except List.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except MultiValueDictKeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    serializer = memberSerializer(members, context={'request': request}, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([canShow])
def getAllMemberByIsPay(request):

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
        return Response(status=status.HTTP_404_NOT_FOUND)
    except MultiValueDictKeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    serializer = memberSerializer(members, context={'request': request}, many=True)
    return Response(serializer.data)

#-----------------------POST-------------------------
@api_view(['POST'])
@permission_classes([canCreate])
def postList(request):

    serializer = listSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([canCreate])
def postMember(request):

    serializer = memberSerializer(data=request.data, context={'request': request}, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#-----------------------PATCH-------------------------
@api_view(['PATCH'])
@permission_classes([canCreate])
def editList(request, pk):

    try:
        lists = List.objects.get(pk=pk)
    except List.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = listSerializer(lists,data=request.data, context={'request': request}, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([canCreate])
def editMember(request, pk):

    try:
        members = Member.objects.get(pk=pk)
    except Member.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = memberSerializer(members,data=request.data, context={'request': request}, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#-----------------------DELETE------------------------
@api_view(['DELETE'])
@permission_classes([canCreate])
def delList(request, pk):

    try:
        lists = List.objects.get(pk=pk)
    except List.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    lists.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
@permission_classes([canCreate])
def delMember(request, pk):

    try:
        members = Member.objects.get(pk=pk)
    except Member.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    members.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)