from rest_framework import permissions

from users.utility import getUser, userHasPerm


class canGetTimetable(permissions.BasePermission):

    def has_permission(self, request, view):
        return userHasPerm(request, "timetable.view_lesson")


class canSetTimetable(permissions.BasePermission):

    def has_permission(self, request, view):
        return userHasPerm(request, "timetable.add_lesson")


class canSetHourLesson(permissions.BasePermission):

    def has_permission(self, request, view):
        return userHasPerm(request, "timetable.add_hourlesson")
