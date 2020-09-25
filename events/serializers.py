from rest_framework import serializers
from events.models import event, type
from django.utils import timezone

class eventSerializerDetail(serializers.ModelSerializer):

    class Meta:
        model = event
        fields = ['pk','name','description','eventType','dateStart','dateEnd','group']

    def create(self, validated_data):

        if 'dateStart' in validated_data and 'dateEnd' in validated_data:
            if validated_data['dateStart'] > validated_data['dateEnd']:
                 raise serializers.ValidationError({'dateStart': 'This field is must be smaller then dateEnd.'})         
        elif 'dateStart' in validated_data:
            if validated_data['dateStart'] > timezone.now():
                raise serializers.ValidationError({'dateStart': 'This field is must be smaller then dateEnd (it\'s set to now).'})
        elif 'dateEnd' in validated_data:
            if validated_data['dateEnd'] < timezone.now():
                raise serializers.ValidationError({'dateEnd': 'This field is must be biger then dateStart (it\'s set to now).'})
        
        events = event.objects.create(**validated_data)
        return events
        
class eventSerializer(serializers.ModelSerializer):

    class Meta:
        model = event
        fields = ['pk','name','eventType','dateStart','dateEnd','group']
        

class typeSerializer(serializers.ModelSerializer):

    class Meta:
        model = type
        fields = ['pk','name','color']
