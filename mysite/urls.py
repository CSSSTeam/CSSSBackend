from django.urls import include, path
from rest_framework import routers
from users import views as viewsUsers
from fileSystem import views as viewsFile
from rest_framework.authtoken.views import ObtainAuthToken
from users import urls as usersUrls
router = routers.DefaultRouter()
router.register(r'files', viewsFile.fileViewSet)
router.register(r'types', viewsFile.typesViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', ObtainAuthToken.as_view()),
    path('user/', include(usersUrls))
]