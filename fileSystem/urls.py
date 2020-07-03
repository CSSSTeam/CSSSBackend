from django.urls import include, path

from fileSystem.views import (
    AllFile, AllFileType, File, FileByType, FileType, SearchFile, UploadFile,
    UploadFileComplete)

urlpatterns = [
    path('file/', AllFile.as_view()),
    path('file/<int:pk>/', File.as_view()),
    path('file/search/', SearchFile.as_view()),
    path('file/type/', FileByType.as_view()),

    path('type/', AllFileType.as_view()),
    path('type/<int:pk>/', FileType.as_view()),

    path('file/upload/complete/', UploadFileComplete.as_view(), name='api_chunked_upload_complete'),
    path('file/upload/', UploadFile.as_view()),
]
