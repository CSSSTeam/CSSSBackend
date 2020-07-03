from django.urls import include, path

from treasurer.views import (AllList, AllMember, MemberByIsPay, MemberByUser,
                             vList, vMember)

urlpatterns = [
    path('list/', AllList.as_view()),
    path('list/<int:pk>/', vList.as_view()),

    path('member/', AllMember.as_view()),
    path('member/<int:pk>/', vMember.as_view()),
    path('member/pay/', MemberByIsPay.as_view()),
    path('member/user/', MemberByUser.as_view()),
]
