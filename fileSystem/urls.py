from django.urls import include, path
from fileSystem.views import getFile, getFileByType, getAllFile, postFile, getType, getAllType, postType, editFile, editType, delType, delFile, searchFile

urlpatterns = [
    path('file/<int:pk>/', getFile),
    path('file/', getAllFile),
    path('file/search/', searchFile),
    path('file/type/', getFileByType),
    path('type/<int:pk>/', getType),
    path('type/', getAllType),

    path('file/add/', postFile),
    path('file/edit/<int:pk>/', editFile),
    path('type/add/', postType),
    path('type/edit/<int:pk>/', editType),
    
    path('file/del/<int:pk>/', delFile),
    path('type/del/<int:pk>/', delType),
]