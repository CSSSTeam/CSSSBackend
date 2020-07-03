import os
from django.db.models import Q
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from fileSystem.permission import fileSystemPerm
from fileSystem.serializers import fileSerializer, typeSerializer, fileSerializerDetail
from fileSystem.models import file, type, MyChunkedUpload

from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView

from fileSystem.googleUpload import upload2drive


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

        try:
            os.remove(files.upload)
            files.delete()
        except Exception as e:
            return Response(settings.ERROR_MESSAGE_DEL, status=status.HTTP_404_NOT_FOUND)

        return Response(settings.ERROR_MESSAGE_204, status=status.HTTP_204_NO_CONTENT)


class AllFile(APIView):
    permission_classes = [fileSystemPerm]

    def get(self, request):
        try:
            files = file.objects.all()
        except file.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404, status=status.HTTP_404_NOT_FOUND)

        serializer = fileSerializer(files, context={'request': request}, many=True)
        return Response(serializer.data)


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


# ------------ Uploading file -----------
class UploadFile(ChunkedUploadView):
    model = MyChunkedUpload
    field_name = 'the_file'

    def check_permissions(self, request):
        if not fileSystemPerm:
            return Response(status=status.HTTP_403_FORBIDDEN)


class UploadFileComplete(ChunkedUploadCompleteView):
    response: str
    model = MyChunkedUpload
    field_name = 'the_file'

    def check_permissions(self, request):
        if not fileSystemPerm:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def on_completion(self, uploaded_file, request):
        name = uploaded_file.name
        path = settings.MEDIA_ROOT + name
        SaveFile(path, uploaded_file)
        downloadUrl = upload2drive(name, path)
        if downloadUrl is None:
            downloadUrl = request.build_absolute_uri(settings.MEDIA_URL+name)
        f = file.objects.create(name=name, upload=downloadUrl)
        f.save()
        serializer = fileSerializer(f)
        self.response = serializer.data

    def get_response_data(self, chunked_upload, request):
        return self.response


# ------------ Save file ------------
def SaveFile(name, f):
    with open(name, 'wb+') as destination:
        i = 0
        for chunk in f.chunks():
            destination.write(chunk)
            print("Saving... [" + str(i) + " chunk]")
            i += 1
        print("File saved! [DONE]")
    return name
