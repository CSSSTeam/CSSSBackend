from django.db.models import Q
from datetime import datetime
from django.utils.datastructures import MultiValueDictKeyError

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from fileSystem.permission import canCreate, canShow
from events.serializers import eventSerializer, typeSerializer, eventSerializerDetail
from events.models import event, type

#------------------------GET-------------------------

#-----------Type-----------
@api_view(['GET'])
@permission_classes([canShow])
def getType(request, pk, format=None):

    try:
        types = type.objects.get(pk=pk)
    except type.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = typeSerializer(types, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([canShow])
def getAllType(request, format=None):

    try:
        types = type.objects.all()
    except type.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = typeSerializer(types, context={'request': request}, many=True)
    return Response(serializer.data)


#-----------event-----------
@api_view(['GET'])
@permission_classes([canShow])
def getEvent(request, pk, format=None):

    try:
        events = event.objects.get(pk=pk)
    except event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = eventSerializerDetail(events, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([canShow])
def getEventByMonth(request, format=None):

    try:
        m = request.GET['m']
        y = request.GET['y']

        events = event.objects.filter(Q(dateStart__year=int(y),dateStart__month=int(m)) | Q(dateStart__year=int(y),dateStart__month=int(m)))
    except event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except MultiValueDictKeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    serializer = eventSerializer(events, context={'request': request}, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([canShow])
def getEventByDate(request, format=None):

    try:

        s = datetime.strptime(request.GET['start'], '%Y-%m-%d')
        e = datetime.strptime(request.GET['end'], '%Y-%m-%d')

        events = event.objects.filter( Q(dateEnd__gte=s,dateStart__lte=s) | Q(dateEnd__gte=e,dateStart__lte=e))
    except event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except (ValueError, MultiValueDictKeyError):
        return Response(status=status.HTTP_400_BAD_REQUEST)
 

    serializer = eventSerializer(events, context={'request': request}, many=True)
    return Response(serializer.data)

#------------------------POST-------------------------
@api_view(['POST'])
@permission_classes([canCreate])
def postEvent(request, format=None):

    serializer = eventSerializerDetail(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([canCreate])
def postType(request, format=None):

    serializer = typeSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)