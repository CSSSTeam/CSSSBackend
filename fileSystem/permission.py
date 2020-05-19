from rest_framework import permissions

from users.utility import userHasPerm


class canShow(permissions.BasePermission):

    def has_permission(self, request, view):
        return userHasPerm(request, "fileSystem.can_show_fileSystem")

class canCreate(permissions.BasePermission):

    def has_permission(self, request, view):
        return userHasPerm(request, "fileSystem.can_create_fileSystem")
