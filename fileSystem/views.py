from django.db.models import Q
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser

from fileSystem.permission import fileSystemPerm
from fileSystem.serializers import fileSerializer, typeSerializer, fileSerializerDetail
from fileSystem.models import file, type


# ----------------------------TYPE--------------------------------

class FileType(APIView):
    permission_classes = [fileSystemPerm]

    def get(self, request, pk):
        try:
            types = type.objects.get(pk=pk)
        except type.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404, status=status.HTTP_404_NOT_FOUND)

        serializer = typeSerializer(types, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, pk):
        try:
            types = type.objects.get(pk=pk)
        except type.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404, status=status.HTTP_404_NOT_FOUND)

        serializer = typeSerializer(types, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            types = type.objects.get(pk=pk)
        except type.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404, status=status.HTTP_404_NOT_FOUND)

        types.delete()
        return Response(settings.ERROR_MESSAGE_204, status=status.HTTP_204_NO_CONTENT)

class AllFileType(APIView):
    permission_classes = [fileSystemPerm]

    def get(self, request):
        try:
            types = type.objects.all()
        except type.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404, status=status.HTTP_404_NOT_FOUND)

        serializer = typeSerializer(types, context={'request': request}, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = typeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------------------FILE--------------------------------

class File(APIView):
    permission_classes = [fileSystemPerm]

    def get(self, request, pk):
        try:
            files = file.objects.get(pk=pk)
        except file.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404, status=status.HTTP_404_NOT_FOUND)

        serializer = fileSerializerDetail(files, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, pk):
        try:
            files = file.objects.get(pk=pk)
        except file.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404, status=status.HTTP_404_NOT_FOUND)

        serializer = fileSerializerDetail(files, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            files = file.objects.get(pk=pk)
        except file.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404, status=status.HTTP_404_NOT_FOUND)

        files.delete()
        return Response(settings.ERROR_MESSAGE_204, status=status.HTTP_204_NO_CONTENT)

class AllFile(APIView):
    permission_classes = [fileSystemPerm]
    #parser_classes = [FileUploadParser]

    def get(self, request):
        try:
            files = file.objects.all()
        except file.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404, status=status.HTTP_404_NOT_FOUND)

        serializer = fileSerializer(files, context={'request': request}, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            f = request.FILES['upload']
        except MultiValueDictKeyError:
            return Response(settings.ERROR_MESSAGE_400, status=status.HTTP_400_BAD_REQUEST)

        request.data['upload'] = str(request.data['upload'])
        serializer = fileSerializerDetail(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            SaveFile(settings.MEDIA_ROOT + request.data['upload'], f)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FileByType(APIView):
    permission_classes = [fileSystemPerm]

    def get(self, request):
        try:
            t = request.GET['type']

            files = file.objects.filter(fileType=t)
        except file.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404, status=status.HTTP_404_NOT_FOUND)
        except MultiValueDictKeyError:
            return Response(settings.ERROR_MESSAGE_400, status=status.HTTP_400_BAD_REQUEST)

        serializer = fileSerializerDetail(files, context={'request': request}, many=True)
        return Response(serializer.data)

class SearchFile(APIView):
    permission_classes = [fileSystemPerm]

    def get(self, request):
        try:
            s = request.GET['phrase']

            files = file.objects.filter(Q(name__contains=s) or Q(description__contains=s))
        except file.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404, status=status.HTTP_404_NOT_FOUND)
        except MultiValueDictKeyError:
            return Response(settings.ERROR_MESSAGE_400, status=status.HTTP_400_BAD_REQUEST)

        serializer = fileSerializer(files, many=True)
        return Response(serializer.data)

# ------------ Save file ------------
def SaveFile(name, f):
    with open(name, 'wb+') as destination:
        i=0
        for chunk in f.chunks():
            destination.write(chunk)
            print("Uploading... ["+str(i)+" chunk]")
            i+=1
        print("Uploading... [DONE]")
    return name
