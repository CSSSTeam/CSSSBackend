from treasurer.models import TreasurerList, Member


def createTreasurerList(name, cost, members):
    treasurer_list = TreasurerList(name=name, cost=cost)
    treasurer_list.save()

    for member in members:
        member_object = Member(user=member, isPay=False, treasurerList=treasurer_list)
        member_object.save()
