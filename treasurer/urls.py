from django.urls import include, path
from treasurer.views import getAllLists, getAllMemberByIsPay, getAllMemberByUser, getAllMemberByList

urlpatterns = [
    path('list/', getAllLists),
    path('member/pay/', getAllMemberByIsPay),
    path('member/user/', getAllMemberByIsUser),
    path('member/list/', getAllMemberByList),
]
