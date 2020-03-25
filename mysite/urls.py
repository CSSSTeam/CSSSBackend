from django.conf.urls import url
from django.urls import include, path
from django.views.generic.base import TemplateView
from rest_framework import routers
from rest_framework.authtoken.views import ObtainAuthToken
from django.db.utils import ProgrammingError
from django.contrib.auth.models import Group

from users import urlsUser as usersUrls
from users import urlsGroup as groupsUrls
from fileSystem import urls as fileSystemUrls
from events import urls as eventsUrls
from timetable import urls as timetableURLs
from treasurer import urls as treasurerURLs
from other import urls as otherURLs

urlpatterns = [
    path('auth/', ObtainAuthToken.as_view()),
    path('user/', include(usersUrls)),
    path('fileSystem/', include(fileSystemUrls)),
    path('events/', include(eventsUrls)),
    path('group/', include(groupsUrls)),
    path('timetable/', include(timetableURLs)),
    path('treasurer/', include(treasurerURLs)),
    path('servis/', include(otherURLs)),
    url(r'^.*', TemplateView.as_view(template_name="index.html"), name="home")
]

#------------------------------Subsystems------------------------------
from mysite import generateData

flag = True;
try:
    codeGroups = {
        "eng1": Group.objects.get(name="English Group 1").id,
        "eng2": Group.objects.get(name="English Group 2").id,
        "grm1": Group.objects.get(name="Germany Group 1").id,
        "grm2": Group.objects.get(name="Germany Group 2").id,
        "prac1": Group.objects.get(name="utk1").id,
        "prac2": Group.objects.get(name="utk2").id,
        "prac3": Group.objects.get(name="utk3").id,
        "wf1": Group.objects.get(name="wf1").id,
        "wf2": Group.objects.get(name="wf2").id,
        "wf3": Group.objects.get(name="wfGirls").id
    }
except (ProgrammingError, Group.DoesNotExist):
    flag = False;

if(flag):
    import mysite.subsystems as threadSystem
    threadSystem.startTreading()