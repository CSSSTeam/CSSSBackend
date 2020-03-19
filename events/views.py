import calendar
from datetime import datetime

from django.db.models import Q
from django.utils.datastructures import MultiValueDictKeyError
from django.utils import timezone

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from events.permission import canCreate, canShow
from events.serializers import eventSerializer, typeSerializer, eventSerializerDetail
from events.models import event, type


#-----------Type-----------
@api_view(['GET'])
@permission_classes([canShow])
def getType(request, pk):

    try:
        types = type.objects.get(pk=pk)
    except type.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = typeSerializer(types, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([canShow])
def getAllType(request):

    try:
        types = type.objects.all()
    except type.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = typeSerializer(types, context={'request': request}, many=True)
    return Response(serializer.data)


#-----------event-----------
@api_view(['GET'])
@permission_classes([canShow])
def getEvent(request, pk):

    try:
        events = event.objects.get(pk=pk)
    except event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = eventSerializerDetail(events, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([canShow])
def getEventByMonth(request):

    g = request.GET.get('group')
    print(g)
    try:
       
        m = int(request.GET['m'])
        y = int(request.GET['y'])

        EndDay = calendar.monthrange(y,m)[1]

        s = datetime(year=y,month=m,day=1)
        e = datetime(year=y,month=m,day=EndDay)

        query = Q(dateEnd__gte=s,dateStart__lte=s) or Q(dateEnd__gte=e,dateStart__lte=e) or Q(dateEnd__lte=e,dateStart__gte=s)

        if(g is None):
            events = event.objects.filter(query)
        else:
            events = event.objects.filter(query,group=g)
    except event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except (ValueError, MultiValueDictKeyError):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    serializer = eventSerializer(events, context={'request': request}, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([canShow])
def getEventByDate(request):

    g = request.GET.get('group')

    try:

        s = datetime.strptime(request.GET['start'], '%Y-%m-%d')
        e = datetime.strptime(request.GET['end'], '%Y-%m-%d')

        query = Q(dateEnd__gte=s,dateStart__lte=s) or Q(dateEnd__gte=e,dateStart__lte=e) or Q(dateEnd__lte=e,dateStart__gte=s)

        if(g is None):
            events = event.objects.filter(query)
        else:
            events = event.objects.filter(query,group=g)
    except event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except (ValueError, MultiValueDictKeyError):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

    serializer = eventSerializer(events, context={'request': request}, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([canShow])
def searchEvent(request):
    try:
        s = request.GET['phrase']

        events = event.objects.filter(Q(name__contains=s) or Q(description__contains=s))
    except event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except MultiValueDictKeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    serializer = eventSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([canShow])
def getEventByType(request):
    try:
        t = request.GET['type']

        events = event.objects.filter(eventType=t)
    except event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except (ValueError, MultiValueDictKeyError):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    serializer = eventSerializer(events, many=True)
    return Response(serializer.data)

#------------------------POST-------------------------
@api_view(['POST'])
@permission_classes([canCreate])
def postEvent(request):

    serializer = eventSerializerDetail(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([canCreate])
def postType(request):

    serializer = typeSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#-----------------------PATCH-------------------------
@api_view(['PATCH'])
@permission_classes([canCreate])
def editEvent(request, pk):

    try:
        events = event.objects.get(pk=pk)
    except event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = eventSerializerDetail(events,data=request.data, context={'request': request}, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PATCH'])
@permission_classes([canCreate])
def editType(request, pk):

    try:
        types = type.objects.get(pk=pk)
    except type.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = typeSerializer(types,data=request.data, context={'request': request}, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#-----------------------DELETE------------------------
@api_view(['DELETE'])
@permission_classes([canCreate])
def delEvent(request, pk):

    try:
        events = event.objects.get(pk=pk)
    except event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    events.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
@permission_classes([canCreate])
def delType(request, pk):

    try:
        types = type.objects.get(pk=pk)
    except type.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    types.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)