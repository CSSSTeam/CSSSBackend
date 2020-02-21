from django.urls import include, path
from events.views import getEvent, postEvent, getType, getAllType, postType, getEventByMonth, getEventByDate, delEvent, delType, editEvent, editType

urlpatterns = [
    path('event/<int:pk>/', getEvent),
    path('type/<int:pk>/', getType),
    path('type/', getAllType),
    path('event/month/',getEventByMonth),
    path('event/date/',getEventByDate),

    path('event/add/', postEvent),
    path('event/edit/<int:pk>/', editEvent),
    path('type/add/', postType),
    path('type/edit/<int:pk>/', editType),

    path('event/del/<int:pk>/', delEvent),
    path('type/del/<int:pk>/', delType),
]
