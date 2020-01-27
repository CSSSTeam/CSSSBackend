from django.urls import include, path
from timetable.views import setHourLesson, setTimetable

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('createHour/', setHourLesson),
    path('createTimetable/', setTimetable),
]