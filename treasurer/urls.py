from django.urls import include, path
from treasurer.views import getAllList
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('list/', getAllList),
]
