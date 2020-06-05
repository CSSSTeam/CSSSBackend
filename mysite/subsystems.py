from django.db import connection
from django.db.utils import ProgrammingError
from django.contrib.auth.models import Group

def table_exists(table_name):
    try:
        return table_name in connection.introspection.table_names()
    except Exception as e: 
        return False

def group_exists(group_name):
    flag = True
    try:
        Group.objects.get(name=group_name)
    except (ProgrammingError, Group.DoesNotExist):
        flag = False
    return flag


if(table_exists("auth_user")):
    import mysite.generateData as generateData
    generateData.startTreading()
    
if(group_exists("English Group 1")):
    import mysite.generateTimetable as generateTimetable
    generateTimetable.startTreading()