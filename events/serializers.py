from rest_framework import serializers
from events.models import event, type

class eventSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = event
        fields = ['name','description','eventType','date','group']
        

class typeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = type
        fields = ['name']
