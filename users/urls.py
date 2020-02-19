from django.urls import include, path
from users.views import detailsUser, logout, AdministrationUser, currentUserAdmin

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('details/', detailsUser.as_view()),
    path('logout/', logout.as_view()),
    path('administration/<int:pk>/', currentUserAdmin.as_view()),
    path('administration/', AdministrationUser.as_view())
]
