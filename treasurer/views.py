# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from treasurer.models import TreasurerList, Member
from treasurer.permission import canGetAllTreasurerLists


@api_view(['GET'])
@permission_classes([canGetAllTreasurerLists])
def getAllList(request):
    treasurer_lists = TreasurerList.objects.all()
    result = []
    for treasurer_list in treasurer_lists:
        list_json = {"name": treasurer_list.name, "cost": treasurer_list.cost}
        members = []
        for member in Member.objects.filter(treasurerList=treasurer_list):
            mem = {"firstName": member.user.first_name, "lastName": member.user.last_name, "isPay": member.isPay}
            members.append(mem)
        list_json["members"] = members
        result.append(list_json)
    return Response(result)
