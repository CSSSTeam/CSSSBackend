from rest_framework import serializers
from treasurer.models import TreasurerList, Member

class treasurerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = TreasurerList
        fields = ['pk','name','cost']
        
class memberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = ['pk','name','isPay','treasurerList']
