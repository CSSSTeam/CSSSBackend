from django.urls import include, path
from treasurer.views import getAllLists, getAllMemberByIsPay, getAllMemberByUser, getAllMemberByList, postMember, postList, editList, editMember, delMember, delList

urlpatterns = [
    path('list/', getAllLists),
    path('member/pay/', getAllMemberByIsPay),
    path('member/user/', getAllMemberByIsUser),
    path('member/list/', getAllMemberByList),

    path('list/add/', postList),
    path('member/add/', postMember),

    path('list/edit/<int:pk>/', editList),
    path('member/edit/<int:pk>/', editMember),

    path('list/del/<int:pk>/', delList),    
    path('member/del/<int:pk>/', delMember),
]
