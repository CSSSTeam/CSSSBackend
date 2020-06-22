from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from other.permission import canShow


#------------------------GET-------------------------
@api_view(['GET'])
@permission_classes([canShow])
def now(request):
    response = {"date": timezone.now()}
    return Response(response)
