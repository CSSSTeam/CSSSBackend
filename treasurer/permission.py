from rest_framework import permissions
from users.utility import userHasPerm


class canShow(permissions.BasePermission):

    def has_permission(self, request, view):
        return userHasPerm("treasurer.show")

class canCreate(permissions.BasePermission):

    def has_permission(self, request, view):
        return userHasPerm("treasurer.create")
