from django.urls import include, path
from fileSystem.views import showFlie

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('filedetal/', showFlie.as_view()),
]