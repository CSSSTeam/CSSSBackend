import calendar
from datetime import datetime

from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from events.models import event, type
from events.permission import EventsPerm
from events.serializers import (eventSerializer, eventSerializerDetail,
                                typeSerializer)

# ----------------------------TYPE--------------------------------

class EventType(APIView):
    permission_classes = [EventsPerm]

    def get(self, request, id):
        try:
            types = type.objects.get(id=id)
        except type.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404,status=status.HTTP_404_NOT_FOUND)

        serializer = typeSerializer(types, context={'request': request})
        return Response(serializer.data)

    def post(self, request, id):
        try:
            types = type.objects.get(id=id)
        except type.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404,status=status.HTTP_404_NOT_FOUND)

        serializer = typeSerializer(types,data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            types = type.objects.get(id=id)
        except type.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404,status=status.HTTP_404_NOT_FOUND)
        
        events = None
        try:
            events = event.objects.filter(eventType=id)
        except event.DoesNotExist:
            pass

        events.delete()
        types.delete()
        return Response(settings.ERROR_MESSAGE_204,status=status.HTTP_204_NO_CONTENT)

class AllEventType(APIView):
    permission_classes = [EventsPerm]

    def get(self, request):
        try:
            types = type.objects.all()
        except type.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404,status=status.HTTP_404_NOT_FOUND)

        serializer = typeSerializer(types, context={'request': request}, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = typeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ----------------------------EVENT--------------------------------

class Event(APIView):
    permission_classes = [EventsPerm]

    def get(self, request, id):

        try:
            events = event.objects.get(id=id)
        except event.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404,status=status.HTTP_404_NOT_FOUND)
    
        serializer = eventSerializerDetail(events, context={'request': request})
        return Response(serializer.data)

    def post(self, request, id):
        try:
            events = event.objects.get(id=id)
        except event.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404,status=status.HTTP_404_NOT_FOUND)

        serializer = eventSerializerDetail(events,data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            events = event.objects.get(id=id)
        except event.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404,status=status.HTTP_404_NOT_FOUND)

        events.delete()
        return Response(settings.ERROR_MESSAGE_204,status=status.HTTP_204_NO_CONTENT)

class AllEvent(APIView):
    permission_classes = [EventsPerm]

    def get(self, request):

        g = request.GET.get('group')
        t = request.GET.get('type')

        try:

            s = datetime.strptime(request.GET['start'], '%Y-%m-%d')
            e = datetime.strptime(request.GET['end'], '%Y-%m-%d')

            if(s>e):
                return Response(status=status.HTTP_400_BAD_REQUEST)

            query = Q(dateEnd__gte=s,dateStart__lte=e) or Q(dateEnd__gte=s,dateStart__lte=e) or Q(dateEnd__gte=e,dateStart__lte=s)

            if(g is None):
                if(t is None):
                    events = event.objects.filter(query)
                else:
                    events = event.objects.filter(query,eventType=t)
            else:
                 if(t is None):
                    events = event.objects.filter(query,group=g)
                 else:
                    events = event.objects.filter(query,group=g,eventType=t)

        except event.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404,status=status.HTTP_404_NOT_FOUND)
        except (ValueError, MultiValueDictKeyError):
            return Response(settings.ERROR_MESSAGE_400,status=status.HTTP_400_BAD_REQUEST)
    

        serializer = eventSerializer(events, context={'request': request}, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = eventSerializerDetail(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventByMonth(APIView):
    permission_classes = [EventsPerm]

    def get(self, request):

        g = request.GET.get('group')
        t = request.GET.get('type')
        print(g)
        try:
       
            m = int(request.GET['m'])
            y = int(request.GET['y'])

            EndDay = calendar.monthrange(y,m)[1]

            s = datetime(year=y,month=m,day=1)
            e = datetime(year=y,month=m,day=EndDay)

            query = Q(dateEnd__gte=s,dateStart__lte=e) or Q(dateEnd__gte=s,dateStart__lte=e) or Q(dateEnd__gte=e,dateStart__lte=s)

            if(g is None):
                if(t is None):
                    events = event.objects.filter(query)
                else:
                    events = event.objects.filter(query,eventType=t)
            else:
                 if(t is None):
                    events = event.objects.filter(query,group=g)
                 else:
                    events = event.objects.filter(query,group=g,eventType=t)

        except event.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404,status=status.HTTP_404_NOT_FOUND)
        except (ValueError, MultiValueDictKeyError):
            return Response(settings.ERROR_MESSAGE_400,status=status.HTTP_400_BAD_REQUEST)

        serializer = eventSerializer(events, context={'request': request}, many=True)
        return Response(serializer.data)

class SearchEvent(APIView):
    permission_classes = [EventsPerm]

    def get(self, request):

        g = request.GET.get('group')
        t = request.GET.get('type')

        try:
            s = request.GET['phrase']
        
            query = Q(name__contains=s) or Q(description__contains=s)

            if(g is None):
                if(t is None):
                    events = event.objects.filter(query)
                else:
                    events = event.objects.filter(query,eventType=t)
            else:
                 if(t is None):
                    events = event.objects.filter(query,group=g)
                 else:
                    events = event.objects.filter(query,group=g,eventType=t)

        except event.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404,status=status.HTTP_404_NOT_FOUND)
        except MultiValueDictKeyError:
            return Response(settings.ERROR_MESSAGE_400,status=status.HTTP_400_BAD_REQUEST)

        serializer = eventSerializer(events, many=True)
        return Response(serializer.data)

class EventByType(APIView):
    permission_classes = [EventsPerm]

    def get(self, request):
        try:
            t = request.GET['type']

            events = event.objects.filter(eventType=t)
        except event.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404,status=status.HTTP_404_NOT_FOUND)
        except (ValueError, MultiValueDictKeyError):
            return Response(settings.ERROR_MESSAGE_400,status=status.HTTP_400_BAD_REQUEST)

        serializer = eventSerializer(events, many=True)
        return Response(serializer.data)
