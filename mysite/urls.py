from django.conf.urls import url
from django.urls import include, path
from django.views.generic.base import TemplateView
from rest_framework import routers
from rest_framework.authtoken.views import ObtainAuthToken
from users import views as viewsUsers
from users import urls as usersUrls
from fileSystem import urls as fileSystemUrls
from events import urls as eventsUrls
from users import urlsGroup as groupsUrls
from timetable import urls as timetableURLs
import mysite.subsystems
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('auth/', ObtainAuthToken.as_view()),
    path('user/', include(usersUrls)),
    path('fileSystem/', include(fileSystemUrls)),
    path('events/', include(eventsUrls)),
    path('group/', include(groupsUrls)),
    path('timetable/', include(timetableURLs)),
    url(r'^.*', TemplateView.as_view(template_name="index.html"), name="home")
]