from django.urls import include, path
from rest_framework.authtoken.views import ObtainAuthToken

from treasurer import urls as treasurerUrls
from users import urls as usersUrls

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('auth/', ObtainAuthToken.as_view()),
    path('user/', include(usersUrls)),
    path('treasurer/', include(treasurerUrls)),
]