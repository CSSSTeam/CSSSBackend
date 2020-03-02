from django.conf.urls import url
from django.urls import include, path
from django.views.generic.base import TemplateView
from rest_framework.authtoken.views import ObtainAuthToken

from events import urls as eventsUrls
from fileSystem import urls as fileSystemUrls
from timetable import urls as timetableURLs
from users import urlsGroup as groupsUrls
from users import urlsUser as usersUrls

from mysite.subsystems import startTreading

startTreading()
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