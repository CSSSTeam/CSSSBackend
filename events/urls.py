from django.urls import include, path
from events.views import Event, AllEvent, EventByType, EventByMonth, SearchEvent, EventType, AllEventType

urlpatterns = [
    path('event/', AllEvent.as_view()),
    path('event/<int:pk>/', Event.as_view()),
    path('event/month/', EventByMonth.as_view()),
    path('event/search/', SearchEvent.as_view()),
    path('event/type/', EventByType.as_view()),

    path('type/', AllEventType.as_view()),
    path('type/<int:pk>/', EventType.as_view()),
]
