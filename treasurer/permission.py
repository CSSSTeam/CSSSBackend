from rest_framework import permissions
from users.utility import userHasPerm


class canShow(permissions.BasePermission):

    def has_permission(self, request, view):
        return userHasPerm(request, "treasurer.can_show_treasurer")

class canCreate(permissions.BasePermission):

    def has_permission(self, request, view):
        return userHasPerm(request, "treasurer.can_create_treasurer")
