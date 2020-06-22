from django.urls import include, path

from timetable.views import getMyTimetable, setHourLessons, setTimetable

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('createHour/', setHourLessons),
    path('createTimetable/', setTimetable),
    path('get/', getMyTimetable),
]
