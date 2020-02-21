from rest_framework import permissions

from users.utility import getUser, userHasPerm


class canShow(permissions.BasePermission):

    def has_permission(self, request, view):
        return True
        return userHasPerm(request, "filesystem.show")

class canCreate(permissions.BasePermission):

    def has_permission(self, request, view):
        return True
        return userHasPerm(request, "filesystem.create")
