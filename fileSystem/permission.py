from rest_framework import permissions
from users.utility import userHasPerm

class fileSystemPerm(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == "GET":
            return userHasPerm(request, "fileSystem.can_show_fileSystem")
        else:
            return userHasPerm(request, "fileSystem.can_create_fileSystem")
