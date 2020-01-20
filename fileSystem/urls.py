from django.urls import include, path
from fileSystem.views import GetFile, PostFile

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('file/<int:pk>/', GetFile.as_view()),
    path('type/<int:pk>/', GetFile.as_view()),
    path('add/', PostFile.as_view()),
]