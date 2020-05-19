from rest_framework import serializers
from fileSystem.models import file, type

class fileSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = file
        fields = ['pk', 'name', 'description', 'upload', 'fileType', 'date', 'author']

class fileSerializer(serializers.ModelSerializer):

    class Meta:
        model = file
        fields = ['pk', 'name', 'upload', 'fileType']
        

class typeSerializer(serializers.ModelSerializer):
    class Meta:
        model = type
        fields = ['pk','name']
