from rest_framework import serializers
from fileSystem.models import file, types

class fileSerializerDetail(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = file
        fields = ['pk','name','description','fileType','upload','date']

class fileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = file
        fields = ['pk','name']
        

class typesSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = types
        fields = ['pk','name']

