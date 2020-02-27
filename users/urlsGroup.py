from django.urls import include, path
from users.views import detailsUser, logout, currentGroupAdmin,AdministrationGroup

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('<int:pk>/', currentGroupAdmin.as_view()),
    path('/', AdministrationGroup.as_view())
]
