from rest_framework import serializers
from events.models import event, type

class eventSerializerDetail(serializers.ModelSerializer):

    class Meta:
        model = event
        fields = ['pk','name','description','eventType','dateStart','dateEnd','group']
        
class eventSerializer(serializers.ModelSerializer):

    class Meta:
        model = event
        fields = ['pk','name','eventType','dateStart','dateEnd','group']
        

class typeSerializer(serializers.ModelSerializer):

    class Meta:
        model = type
        fields = ['pk','name','color']
