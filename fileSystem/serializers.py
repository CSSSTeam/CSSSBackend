from rest_framework import serializers
from fileSystem.models import file, types

class fileSerializerDetail(serializers.ModelSerializer):

    class Meta:
        model = file
        fields = ['pk','name','description','fileType','upload','date']

class fileSerializer(serializers.ModelSerializer):

    class Meta:
        model = file
        fields = ['pk','name','fileType']
        

class typesSerializer(serializers.ModelSerializer):

    class Meta:
        model = types
        fields = ['pk','name']

