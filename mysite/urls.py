from django.conf.urls import url
from django.urls import include, path
from django.views.generic.base import TemplateView
from rest_framework import routers
from rest_framework.authtoken.views import ObtainAuthToken

from users import urlsUser as usersUrls
from users import urlsGroup as groupsUrls
from fileSystem import urls as fileSystemUrls
from events import urls as eventsUrls
from timetable import urls as timetableURLs
from treasurer import urls as treasurerURLs

import mysite.subsystems

urlpatterns = [
    path('auth/', ObtainAuthToken.as_view()),
    path('user/', include(usersUrls)),
    path('fileSystem/', include(fileSystemUrls)),
    path('events/', include(eventsUrls)),
    path('group/', include(groupsUrls)),
    path('timetable/', include(timetableURLs)),
    path('treasurer/', include(treasurerURLs)),
    url(r'^.*', TemplateView.as_view(template_name="index.html"), name="home")
]