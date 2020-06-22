from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import include, path
from django.views.generic.base import TemplateView
from django.views.static import serve
from rest_framework import routers
from rest_framework.authtoken.views import ObtainAuthToken

import mysite.subsystems
from events import urls as eventsUrls
from fileSystem import urls as fileSystemUrls
from other import urls as otherURLs
from timetable import urls as timetableURLs
from treasurer import urls as treasurerURLs
from users import urlsGroup as groupsUrls
from users import urlsUser as usersUrls

urlpatterns = [
    path('auth/', ObtainAuthToken.as_view()),
    path('user/', include(usersUrls)),
    path('fileSystem/', include(fileSystemUrls)),
    path('events/', include(eventsUrls)),
    path('group/', include(groupsUrls)),
    path('timetable/', include(timetableURLs)),
    path('treasurer/', include(treasurerURLs)),
    path('servis/', include(otherURLs)),
    url(r'^uploaded_files/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^.*', TemplateView.as_view(template_name="index.html"), name="home")
]
