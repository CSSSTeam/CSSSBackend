from django.urls import include, path
from fileSystem.views import File, FileByType, AllFile, SearchFile, FileType, AllFileType

urlpatterns = [
    path('file/', AllFile.as_view()),
    path('file/<int:pk>/', File.as_view()),
    path('file/search/', SearchFile.as_view()),
    path('file/type/', FileByType.as_view()),

    path('type/', AllFileType.as_view()),
    path('type/<int:pk>/', FileType.as_view()),
]