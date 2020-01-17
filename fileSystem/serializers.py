from rest_framework import serializers
from fileSystem.models import file, types

class fileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = file
        fields = dir(file)

class typesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = types
        fields = dir(types)

