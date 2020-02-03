from django.urls import include, path
from fileSystem.views import getFile, getAllFile, postFile, getType, getAllType, postType

urlpatterns = [
    path('file/<int:pk>/', getFile),
    path('file/', getAllFile),
    path('type/<int:pk>/', getType),
    path('type/', getAllType),
    path('file/add/', postFile),
    path('type/add/', postType),
]