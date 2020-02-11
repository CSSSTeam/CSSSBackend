from rest_framework import permissions

from users.utility import getUser, userHasPerm


class canShowFiles(permissions.BasePermission):

   def has_permission(self, request, view):
        return True #debug
        return userHasPerm(request, "filesystem.show_file")

class canUploadFiles(permissions.BasePermission):

   def has_permission(self, request, view):
        return True #debug
        return userHasPerm(request, "filesystem.uplaod_file")
