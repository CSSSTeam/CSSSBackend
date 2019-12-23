from rest_framework import permissions

from users.utility import getUser


class canOperatingInfo(permissions.BasePermission):

    def has_permission(self, request, view):

        print(request.method)
        if request.method in permissions.SAFE_METHODS:#
            return True
        user = getUser(request)
        if user.has_perm("auth.change_user") and request.method == "POST":
            return True
        return False

