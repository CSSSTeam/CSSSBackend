from rest_framework import permissions
from users.utility import userHasPerm

class EventsPerm(permissions.BasePermission):

   def has_permission(self, request, view):
        if request.method == "GET":
            return userHasPerm(request, "events.can_show_events")
        else:
            return userHasPerm(request, "events.can_create_events")
