from django.urls import include, path

from treasurer.views import (AllList, AllMember, MemberByIsPay, MemberByUser,
                             vList, vMember)

urlpatterns = [
    path('list/', AllList.as_view()),
    path('list/<uuid:id>/', vList.as_view()),

    path('member/', AllMember.as_view()),
    path('member/<uuid:id>/', vMember.as_view()),
    path('member/pay/', MemberByIsPay.as_view()),
    path('member/user/', MemberByUser.as_view()),
]
