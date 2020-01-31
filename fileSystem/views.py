from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from users.permission import canOperatingInfo
from fileSystem.serializers import fileSerializer, typesSerializer
from fileSystem.models import file, types
from rest_framework.parsers import FileUploadParser


class fileViewSet(viewsets.ModelViewSet):
    queryset = file.objects.all()
    serializer_class = fileSerializer


class typesViewSet(viewsets.ModelViewSet):
    queryset = types.objects.all()
    serializer_class = typesSerializer

#------------------------GET-------------------------
        
@api_view(['GET'])

def getType(request, pk, format=None):

    try:
        type = types.objects.get(pk=pk)
    except types.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET':
        serializer =  typesSerializer(type, context={'request': request})
        return Response(serializer.data)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])

def getFile(request, pk, format=None):

    try:
        files = file.objects.get(pk=pk)
    except file.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET':
        serializer =  fileSerializer(files, context={'request': request})
        return Response(serializer.data)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


#------------------------POST-------------------------

@api_view(['POST'])

def postFile(request, format=None):

    #parser_classes = [FileUploadParser]

    if request.method == 'POST':
        serializer =  fileSerializer(data=request.data, context={'request': request})

        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

            f = request.data['file']
            file.upload.save(f.name, f, save=True)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['POST'])

def postType(request, format=None):

    if request.method == 'POST':
        serializer =  typesSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

