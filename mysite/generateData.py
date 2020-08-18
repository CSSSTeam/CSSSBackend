import threading

from django.conf import settings
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from events.models import event
from fileSystem.models import file
from treasurer.models import List


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

def createPerm(permissions=[],models=[],premName=[]):
    i = 0
    for permission in permissions:
        contentType = ContentType.objects.get_for_model(models[i])
        for name in premName:
            perm = Permission.objects.get_or_create(codename=name + permission, name=name + permission + "!", content_type=contentType)
        i+=1

def setUpPerm():
    premNameToCreate = ["can_create_", "can_show_"]
    models = [event, file, List]
    permissionsToCreate=["events", "fileSystem", "treasurer"]

    createPerm(permissions=permissionsToCreate, models=models, premName=premNameToCreate)

def generate():

    setUpPerm()
    
    studentPermissions = ["change_user", "view_lesson","can_show_events","can_show_fileSystem","can_show_treasurer"]
    treasurerPermissions = studentPermissions + ["can_create_treasurer"]
    moderatorPermissions = studentPermissions + ["add_hourlesson", "add_lesson", "view_user", "add_user","delete_user"]
    adminPermissions = moderatorPermissions + ["can_create_events", "can_create_fileSystem", "can_create_treasurer"]

    student = createGroup(name="Student", permissions=studentPermissions)
    treasurer = createGroup(name="Treasurer", permissions=treasurerPermissions)
    president = createGroup(name="President")
    vicePresident = createGroup(name="Vice President")
    moderator = createGroup(name="Moderator", permissions=moderatorPermissions)
    admin = createGroup(name="Admin", permissions=adminPermissions)

    englishGr1 = createGroup(name="English Group 1")
    englishGr2 = createGroup(name="English Group 2")
    germanyGr1 = createGroup(name="Germany Group 1")
    germanyGr2 = createGroup(name="Germany Group 2")
    utk1 = createGroup(name="utk1")
    utk2 = createGroup(name="utk2")
    utk3 = createGroup(name="utk3")
    wf1 = createGroup(name="wf1")
    wf2 = createGroup(name="wf2")
    wfGirls = createGroup(name="wfGirls")

    createUser(username="admin", password="admin", first_name="admin", last_name="toor",
                email="admin@admin.com", groups=[admin, englishGr1, germanyGr2, utk1, wf1])

    if settings.CREATE_DEBUG_USERS
        createUser(username="user1", password="admin", first_name="admin", last_name="toor",
                    email="admin@admin.com", groups=[admin, englishGr1, germanyGr2, utk1, wf1])
        createUser(username="Larry", password="I_hate_apple", first_name="Larry", last_name="Page",
                    email="ihateapple@gmail.com", groups=[moderator, englishGr1, germanyGr1, utk2, wf1])
        createUser(username="user3", password="I_hate_apple", first_name="Siergi", last_name="Brin",
                    email="google@gmail.com", groups=[treasurer, englishGr2, germanyGr2, utk3, wf2])
        createUser(username="Steve", password="apple1234", first_name="Steve", last_name="Jobs",
                    email="stevejobs@apple.com", groups=[student, englishGr2, germanyGr1, utk3, wfGirls])


def treadFunction():
    generate()


def startTreading():
    thread = threading.Thread(target=treadFunction)
    thread.start()
