from django.urls import include, path

from events.views import (AllEvent, AllEventType, Event, EventByMonth,
                          EventByType, EventType, SearchEvent)

urlpatterns = [
    path('event/', AllEvent.as_view()),
    path('event/<uuid:id>/', Event.as_view()),
    path('event/month/', EventByMonth.as_view()),
    path('event/search/', SearchEvent.as_view()),
    path('event/type/', EventByType.as_view()),

    path('type/', AllEventType.as_view()),
    path('type/<uuid:id>/', EventType.as_view()),
]
