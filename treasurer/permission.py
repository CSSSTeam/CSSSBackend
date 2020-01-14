from rest_framework import permissions

from users.utility import getUser


class canGetAllTreasurerLists(permissions.BasePermission):

    def has_permission(self, request, view):
        user = getUser(request)
        print(user)
        if user.has_perm("treasurer.view_treasurerlist"):
            return True
        return False

