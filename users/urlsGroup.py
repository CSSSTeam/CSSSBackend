from django.urls import include, path

from users.views import (AdministrationGroup, currentGroupAdmin, detailsUser,
                         logout)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('<int:pk>/', currentGroupAdmin.as_view()),
    path('', AdministrationGroup.as_view())
]
