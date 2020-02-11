from django.urls import include, path
from events.views import getEvent, postEvent, getType, getAllType, postType, getEventByMonth

urlpatterns = [
    path('event/<int:pk>/', getEvent),
    path('type/<int:pk>/', getType),
    path('type/', getAllType),
    path('event/add/', postEvent),
    path('type/add/', postType),
    path('event/',getEventByMonth)
]
