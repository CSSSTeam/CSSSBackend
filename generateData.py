from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

from treasurer.models import TreasurerList


def createUser(username, password, first_name="", last_name="", email="", groups=[]):
    user = User.objects.get_or_create(username=username)[0]
    user.set_password(raw_password=password)
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    for group in groups:
        user.groups.add(group)
    user.save()


def createGroup(name, permissions=[]):
    group = Group.objects.get_or_create(name=name)[0]
    for permission in permissions:
        perm = Permission.objects.get(codename=permission)
        group.permissions.add(perm)
    group.save()
    return group


def createPerm(model, codename, name, ):
    content_type = ContentType.objects.get_for_model(model)
    permission = Permission.objects.get_or_create(
        codename=codename,
        name=name,
        content_type=content_type,
    )


createPerm(TreasurerList, "view_yourself_treasurerlist","Can view yourself treasurer lists")

studentPermissions = ["change_user", "view_yourself_treasurerlist"]
treasurerPermissions = studentPermissions + ["view_treasurerlist", "add_treasurerlist", "change_treasurerlist",
                                             "delete_treasurerlist",
                                             "view_member", "add_member", "change_member", "delete_member"]

student = createGroup(name="Student", permissions=studentPermissions)
treasurer = createGroup(name="Treasurer", permissions=treasurerPermissions)
president = createGroup(name="President")
vicePresident = createGroup(name="Vice President")
moderator = createGroup(name="Moderator")
admin = createGroup(name="Admin")
englishGr1 = createGroup(name="English Group 1")
englishGr2 = createGroup(name="English Group 2")
germanyGr1 = createGroup(name="Germany Group 1")
germanyGr2 = createGroup(name="Germany Group 2")
createUser(username="admin", password="admin", first_name="admin", last_name="toor",
           email="admin@admin.com", groups=[admin, englishGr1, germanyGr1])
createUser(username="user", password="user", first_name="user", last_name="orzeszek",
           email="zsl@przyszlosc.com", groups=[treasurer, englishGr2, germanyGr2])
