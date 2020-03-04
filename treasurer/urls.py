from django.urls import include, path
from treasurer.views import getAllList

urlpatterns = [
    path('list/', getAllList),
]
