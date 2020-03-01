from rest_framework import permissions

from users.utility import getUser, userHasPerm


class canAdministionOnCurrent(permissions.BasePermission):
    def has_permission(self, request, view):
        if userHasPerm(request, "auth.view_user") and request.method == "GET":
            return True
        if userHasPerm(request, "auth.delete_user") and request.method == "DELETE":
            return True
        return False


class canAdministionUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if userHasPerm(request, "auth.view_user") and request.method == "GET":
            return True
        if userHasPerm(request, "auth.add_user") and request.method == "POST":
            return True
        return False


class canOperatingInfo(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if userHasPerm(request, "auth.change_user") and request.method == "POST":
            return True
        return False
