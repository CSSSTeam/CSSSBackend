from django.urls import include, path

from other.views import now

urlpatterns = [
        path('now/', now),
    ]
