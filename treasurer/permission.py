from rest_framework import permissions
from users.utility import userHasPerm


class canGetAllTreasurerLists(permissions.BasePermission):

    def has_permission(self, request, view):
        return True
        return userHasPerm("treasurer.view_treasurerlist")
