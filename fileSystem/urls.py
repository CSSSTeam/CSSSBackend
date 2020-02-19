from django.urls import include, path
from fileSystem.views import getFile, getFileByType, getAllFile, postFile, getType, getAllType, postType

urlpatterns = [
    path('file/<int:pk>/', getFile),
    path('file/', getAllFile),
    path('file/type/', getFileByType),
    path('type/<int:pk>/', getType),
    path('type/', getAllType),
    path('file/add/', postFile),
    path('type/add/', postType),
]