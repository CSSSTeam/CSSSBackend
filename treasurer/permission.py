from rest_framework import permissions
from users.utility import userHasPerm


class treasurerPerm(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == "GET":
            return userHasPerm(request, "treasurer.can_show_treasurer")
        else:
            return userHasPerm(request, "treasurer.can_create_treasurer")
