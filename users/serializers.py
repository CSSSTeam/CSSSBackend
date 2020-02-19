from django.contrib.auth.models import Group, User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class UserDisplaySerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    class GroupSerializer(serializers.Serializer):
        def update(self, instance, validated_data):
            pass

        def create(self, validated_data):
            pass

        id = serializers.IntegerField()
        name = serializers.CharField()

    id = serializers.IntegerField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    groups = GroupSerializer(many=True)


class UserSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.CharField()
    groups = UserDisplaySerializer.GroupSerializer(many=True)


class UserCreator(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        groups = None
        if 'groups' in validated_data:
            groups = validated_data['groups']
        del validated_data['groups']
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        if not groups == None:
            for gr in groups:
                group = Group.objects.get(id=gr)
                user.groups.add(group)
        return user

    username = serializers.CharField()
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField()
    groups = serializers.ListField(required=False, child=serializers.IntegerField())
