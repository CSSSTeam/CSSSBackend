from django.contrib.auth.models import Group, Permission
from rest_framework import serializers

from .models import User


class PermissionSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    id = serializers.IntegerField()
    codename = serializers.CharField()


class GroupSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    id = serializers.IntegerField()
    name = serializers.CharField()


class GroupDisplaySerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    id = serializers.IntegerField()
    name = serializers.CharField()
    permissions = PermissionSerializer(many=True)


class GroupCreator(serializers.Serializer):

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        permissions = None
        if 'permissions' in validated_data:
            permissions = validated_data['permissions']
        del validated_data['permissions']
        group = Group.objects.create(**validated_data)
        if permissions is not None:
            for perm in permissions:
                permission = Permission.objects.get(id=perm)
                group.permissions.add(permission)
        return group

    name = serializers.CharField()
    permissions = serializers.ListField(child=serializers.IntegerField())


class UserDisplaySerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    id = serializers.IntegerField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    groups = GroupSerializer(many=True)
    hasChangedPass = serializers.BooleanField()


class UserSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.CharField()
    groups = GroupSerializer(many=True)


class ChangePasswordSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    oldPass = serializers.CharField()
    newPass = serializers.CharField()
    newPass2 = serializers.CharField()


class UserCreator(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', "groups", 'email', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        groups = None
        if 'groups' in validated_data:
            groups = validated_data['groups']
            del validated_data['groups']
        
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])

        if groups is not None:
                for gr in groups:
                    user.groups.add(gr)
        
        return user
