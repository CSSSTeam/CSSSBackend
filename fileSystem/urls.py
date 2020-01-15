from django.urls import include, path
from fileSystem.views import GetFile

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('info/<int:pk>/', GetFile.as_view()),
]