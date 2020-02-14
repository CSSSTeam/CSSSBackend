from rest_framework import serializers
from events.models import event, type

class eventSerializerDetail(serializers.ModelSerializer):

    class Meta:
        model = event
        fields = ['pk','name','description','eventType','dateStart','dateEnd']
        
class eventSerializer(serializers.ModelSerializer):

    class Meta:
        model = event
        fields = ['pk','name','eventType','dateStart','dateEnd']
        

class typeSerializer(serializers.ModelSerializer):

    class Meta:
        model = type
        fields = ['pk','name']
