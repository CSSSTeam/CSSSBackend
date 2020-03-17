from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.utils import timezone

#------------------------GET-------------------------
@api_view(['GET'])
def now(request):
    response = {"date": timezone.now()}
    return Response(response)
