from rest_framework import serializers
from treasurer.models import List, Member

class listSerializer(serializers.ModelSerializer):

    class Meta:
        model = List
        fields = ['pk','name','cost','date']
        
class memberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = ['pk','user','isPay','treasurerList']
