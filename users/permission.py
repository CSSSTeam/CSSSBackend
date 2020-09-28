from rest_framework import permissions

from users.utility import getUser, userHasPerm


class canAdministionOnCurrent(permissions.BasePermission):
    def has_permission(self, request, view):
        if userHasPerm(request, "users.view_user") and request.method == "GET":
            return True
        if userHasPerm(request, "users.delete_user") and request.method == "DELETE":
            return True
        return False


class canAdministionUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if userHasPerm(request, "users.view_user") and request.method == "GET":
            return True
        if userHasPerm(request, "users.add_user") and request.method == "POST":
            return True
        if userHasPerm(request, "users.delete_user") and request.method == "DELETE":
            return True
        return False


class canOperatingInfo(permissions.BasePermission):

    def has_permission(self, request, view):
        if getUser(request) != None:
            return True
        return False
