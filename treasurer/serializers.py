from rest_framework import serializers
from treasurer.models import List, Member

class listSerializer(serializers.ModelSerializer):

    class Meta:
        model = List
        fields = ['pk','name','cost']
        
class memberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = ['pk','name','isPay','treasurerList']
