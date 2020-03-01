from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from treasurer.models import TreasurerList
from fileSystem.models import file, types
from django.utils import timezone



def createUser(username, password, first_name="", last_name="", email="", groups=[]):
    user = User.objects.get_or_create(username=username)[0]
    user.set_password(raw_password=password)
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    for group in groups:
        user.groups.add(group)
    user.save()
    return user


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

def createFile(name="", description="", fileType="", upload="", author=""):
    files = file.objects.get_or_create(name=name, fileType=fileType)[0]
    files.description = description
    files.upload = upload
    files.date = timezone.now()
    files.save()
    return files



def createType(name=""):
    type = types.objects.get_or_create(name=name)[0]
    type.save()
    return type


studentPermissions = ["change_user", "view_lesson"]
treasurerPermissions = studentPermissions
moderatorPermissions = studentPermissions + ["add_hourlesson", "add_lesson"]
student = createGroup(name="Student", permissions=studentPermissions)
treasurer = createGroup(name="Treasurer", permissions=treasurerPermissions)
president = createGroup(name="President")
vicePresident = createGroup(name="Vice President")
moderator = createGroup(name="Moderator", permissions=moderatorPermissions)
admin = createGroup(name="Admin")
englishGr1 = createGroup(name="English Group 1")
englishGr2 = createGroup(name="English Group 2")
germanyGr1 = createGroup(name="Germany Group 1")
germanyGr2 = createGroup(name="Germany Group 2")

user = createUser(username="admin", password="admin", first_name="admin", last_name="toor",
                  email="admin@admin.com", groups=[admin, englishGr1, germanyGr2])
createUser(username="moderator", password="moderator", first_name="Steve", last_name="Jobs",
           email="stevejobs@apple.com", groups=[moderator, englishGr1, germanyGr1])

type = createType("ak")
createFile("bfc", "bc", type, "dx")
