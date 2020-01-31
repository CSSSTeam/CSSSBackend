from django.urls import include, path
from fileSystem.views import getFile, postFile, getType, postType

urlpatterns = [
    path('file/<int:pk>/', getFile),
    path('type/<int:pk>/', getType),
    path('file/add/', postFile),
    path('type/add/', postType),
]