from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from fileSystem.permission import canUploadFiles, canShowFiles
from fileSystem.serializers import fileSerializer, typesSerializer
from fileSystem.models import file, types
from rest_framework.parsers import FileUploadParser
from django.conf import settings


class fileViewSet(viewsets.ModelViewSet):
    queryset = file.objects.all()
    serializer_class = fileSerializer


class typesViewSet(viewsets.ModelViewSet):
    queryset = types.objects.all()
    serializer_class = typesSerializer

#------------------------GET-------------------------
        
#-----------Type-----------

@api_view(['GET'])

def getType(request, pk, format=None):

    permission_classes = [canShowFiles]

    if request.method == 'GET':
        try:
            type = types.objects.get(pk=pk)
        except types.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
        serializer =  typesSerializer(type, context={'request': request})
        return Response(serializer.data)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])

def getAllType(request, format=None):

    permission_classes = [canShowFiles]

    if request.method == 'GET':
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

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

#-----------File-----------

@api_view(['GET'])

def getFile(request, pk, format=None):

    permission_classes = [canShowFiles]
    
    if request.method == 'GET':
        try:
            files = file.objects.get(pk=pk)
        except file.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer =  fileSerializer(files, context={'request': request})
        return Response(serializer.data)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])

def getAllFile(request, format=None):

    if request.method == 'GET':
        permission_classes = [canShowFiles]

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

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


#------------------------POST-------------------------
@api_view(['POST'])

def postFile(request, format=None):

    permission_classes = [canUploadFiles]
    parser_classes = [FileUploadParser]

    if request.method == 'POST':
        f = request.FILES['upload']
        
        request.data['upload']=SaveFile(settings.MEDIA_ROOT+str(request.data['upload']),f)
        
        serializer = fileSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

# Save file
def SaveFile(name,f):

    with open(name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return name
        

@api_view(['POST'])

def postType(request, format=None):

    permission_classes = [canUploadFiles]

    if request.method == 'POST':
        serializer =  typesSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

