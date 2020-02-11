from rest_framework import serializers
from events.models import event, type

class eventSerializerDetail(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = event
        fields = ['pk','name','description','eventType','dateStart','dateEnd']
        
class eventSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = event
        fields = ['pk','name','eventType','dateStart','dateEnd']
        

class typeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = type
        fields = ['pk','name']
