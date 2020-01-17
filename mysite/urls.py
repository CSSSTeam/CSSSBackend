from django.conf.urls import url
from django.urls import include, path
from django.views.generic.base import TemplateView
from rest_framework import routers
from users import views as viewsUsers
from fileSystem import views as viewsFile
from rest_framework.authtoken.views import ObtainAuthToken
from users import urls as usersUrls
from fileSystem import urls as fileUrls

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('auth/', ObtainAuthToken.as_view()),
    path('user/', include(usersUrls)),
    path('file/', include(fileUrls)),
    url(r'^.*', TemplateView.as_view(template_name="index.html"), name="home")
]