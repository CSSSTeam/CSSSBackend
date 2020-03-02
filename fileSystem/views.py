from django.db.models import Q
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError

from fileSystem.permission import canCreate, canShow
from fileSystem.serializers import fileSerializer, typeSerializer, fileSerializerDetail
from fileSystem.models import file, type


# ------------------------GET-------------------------


# -----------Type-----------
@api_view(['GET'])
@permission_classes([canShow])
def getType(request, pk, format=None):
    try:
        types = type.objects.get(pk=pk)
    except type.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = typeSerializer(types, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([canShow])
def getAllType(request, format=None):
    try:
        types = type.objects.all()
    except type.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = typeSerializer(types, context={'request': request}, many=True)
    return Response(serializer.data)


# -----------File-----------
@api_view(['GET'])
@permission_classes([canShow])
def getFile(request, pk, format=None):
    try:
        files = file.objects.get(pk=pk)
    except file.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = fileSerializerDetail(files, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([canShow])
def getFileByType(request, format=None):
    try:
        t = request.GET['type']

        files = file.objects.filter(fileType=t)
    except file.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except MultiValueDictKeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    serializer = fileSerializerDetail(files, context={'request': request}, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([canShow])
def searchFile(request):
    try:
        s = request.GET['phrase']

        files = file.objects.filter(Q(name__contains=s) or Q(description__contains=s))
    except file.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except MultiValueDictKeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    serializer = fileSerializer(files, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([canShow])
def getAllFile(request, format=None):
    try:
        files = file.objects.all()
    except file.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = fileSerializer(files, context={'request': request}, many=True)
    return Response(serializer.data)


# ------------------------POST-------------------------
@api_view(['POST'])
@permission_classes([canCreate])
def postFile(request, format=None):
    parser_classes = [FileUploadParser]

    try:
        f = request.FILES['upload']
    except MultiValueDictKeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    request.data['upload'] = settings.MEDIA_ROOT + str(request.data['upload'])
    serializer = fileSerializerDetail(data=request.data, context={'request': request})

    if serializer.is_valid():
        serializer.save()
        SaveFile(request.data['upload'], f)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Save file
def SaveFile(name, f):
    with open(name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return name


@api_view(['POST'])
@permission_classes([canCreate])
def editFile(request, pk, format=None):
    try:
        files = file.objects.get(pk=pk)
    except file.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = fileSerializerDetail(files, data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([canCreate])
def postType(request, format=None):
    serializer = typeSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([canCreate])
def editType(request, pk, format=None):
    try:
        types = type.objects.get(pk=pk)
    except type.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = typeSerializer(types, data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------DELETE------------------------
@api_view(['DELETE'])
@permission_classes([canCreate])
def delFile(request, pk, format=None):
    try:
        files = file.objects.get(pk=pk)
    except file.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    files.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
@permission_classes([canCreate])
def delType(request, pk, format=None):
    try:
        types = type.objects.get(pk=pk)
    except type.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    types.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
