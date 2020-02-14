from rest_framework import serializers
from fileSystem.models import file, types


class fileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = file
        fields = ['name', 'description', 'fileType', 'upload', 'date']


class typesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = types
        fields = ['name']
