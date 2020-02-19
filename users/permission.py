from rest_framework import permissions

from users.utility import getUser, userHasPerm


class canOperatingInfo(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        if userHasPerm(request, "auth.change_user") and request.method == "POST":
            return True
        return False
