from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from events.serializers import eventSerializer, typeSerializer
from events.models import event, type

#------------------------GET-------------------------

#-----------Type-----------
@api_view(['GET'])
def getType(request, pk, format=None):

    try:
        types = type.objects.get(pk=pk)
    except type.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer =  typeSerializer(types, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def getAllType(request, format=None):

    try:
        types = type.objects.all()
    except type.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    content={}
    for t in types:
        content+={
            'id': t.pk,
            'name': t.name
            }
    return Response(content)

#-----------event-----------
@api_view(['GET'])
def getEvent(request, pk, format=None):

    try:
        events = event.objects.get(pk=pk)
    except event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer =  eventSerializer(events, context={'request': request})
    return Response(serializer.data)

#------------------------POST-------------------------
@api_view(['POST'])
def postEvent(request, format=None):

    serializer =  eventSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def postType(request, format=None):

    serializer =  typeSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)