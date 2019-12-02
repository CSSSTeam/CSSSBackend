from django.urls import include, path
from users.views import detailsUser

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('details/', detailsUser.as_view()),
]