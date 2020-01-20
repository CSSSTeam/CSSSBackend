from rest_framework import permissions

from users.utility import getUser


class canShowFiles(permissions.BasePermission):

    def has_permission(self, request, view):

        print(request.method)
        if request.method in permissions.SAFE_METHODS:
            return True
        user = getUser(request)
        if user.has_perm("auth.show_file") and request.method == "POST":
            return True
        return False

class canUploadFiles(permissions.BasePermission):

    def has_permission(self, request, view):

        print(request.method)
        if request.method in permissions.SAFE_METHODS:
            return True
        user = getUser(request)
        if user.has_perm("auth.uplaod_file") and request.method == "POST":
            return True
        return False
