from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from django.conf import settings

from fileSystem.permission import canUploadFiles, canShowFiles
from fileSystem.serializers import fileSerializer, typesSerializer
from fileSystem.models import file, types


#------------------------GET-------------------------


#-----------Type-----------
@api_view(['GET'])
@permission_classes([canShowFiles])
def getType(request, pk, format=None):

    try:
        type = types.objects.get(pk=pk)
    except types.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer =  typesSerializer(type, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([canShowFiles])
def getAllType(request, format=None):

    try:
        type = types.objects.all()
    except types.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    content={}
    for t in type:
        content+={
            'id': t.pk,
            'name': t.name
            }
    return Response(content)


#-----------File-----------
@api_view(['GET'])
@permission_classes([canShowFiles])
def getFile(request, pk, format=None):

    try:
        files = file.objects.get(pk=pk)
    except file.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer =  fileSerializer(files, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([canShowFiles])
def getAllFile(request, format=None):

    try:
        files = file.objects.all()
    except file.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    content={}
    for f in files:
        content+={
            'id': f.pk,
            'name': f.name
                }
    return Response(content)


#------------------------POST-------------------------
@api_view(['POST'])
@permission_classes([canUploadFiles])
def postFile(request, format=None):

    parser_classes = [FileUploadParser]

    f = request.FILES['upload']
    request.data['upload']=SaveFile(settings.MEDIA_ROOT+str(request.data['upload']),f)
        
    serializer = fileSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Save file
def SaveFile(name,f):

    with open(name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return name
        

@api_view(['POST'])
@permission_classes([canUploadFiles])
def postType(request, format=None):

    serializer =  typesSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
