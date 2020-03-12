from django.urls import include, path
from treasurer.views import getAllLists, getMemberByIsPay, getMemberByUser, getMemberByList, postMember, postList, editList, editMember, delMember, delList, putMember

urlpatterns = [
    path('list/', getAllLists),
    path('member/pay/', getMemberByIsPay),
    path('member/user/', getMemberByUser),
    path('member/list/', getMemberByList),

    path('list/add/', postList),
    path('member/add/', postMember),

    path('member/auto/', putMember),

    path('list/edit/<int:pk>/', editList),
    path('member/edit/<int:pk>/', editMember),

    path('list/del/<int:pk>/', delList),    
    path('member/del/<int:pk>/', delMember),
]
