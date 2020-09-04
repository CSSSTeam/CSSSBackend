from chunked_upload.views import ChunkedUploadCompleteView, ChunkedUploadView
from django.conf import settings
from django.db.models import Q
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MyChunkedUpload, file, type
from .permission import fileSystemPerm
from .serializers import (fileSerializer, fileSerializerDetail,
                                    typeSerializer)

from .fileSave import SaveFileThread
from .googleUpload import upload2driveThread


# ----------------------------TYPE--------------------------------

class FileType(APIView):
    permission_classes = [fileSystemPerm]

    def get(self, request, id):
        try:
            types = type.objects.get(id=id)
        except type.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404, status=status.HTTP_404_NOT_FOUND)

        serializer = typeSerializer(types, context={'request': request})
        return Response(serializer.data)

    def post(self, request, id):
        try:
            types = type.objects.get(id=id)
        except type.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404, status=status.HTTP_404_NOT_FOUND)

        serializer = typeSerializer(types, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            types = type.objects.get(id=id)
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

    def get(self, request, id):
        try:
            files = file.objects.get(id=id)
        except file.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404, status=status.HTTP_404_NOT_FOUND)

        serializer = fileSerializerDetail(files, context={'request': request})
        return Response(serializer.data)

    def post(self, request, id):
        try:
            files = file.objects.get(id=id)
        except file.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404, status=status.HTTP_404_NOT_FOUND)

        serializer = fileSerializerDetail(files, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            files = file.objects.get(id=id)
        except file.DoesNotExist:
            return Response(settings.ERROR_MESSAGE_404, status=status.HTTP_404_NOT_FOUND)

        try:
            if os.path.exists(files.upload):
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

        f = file.objects.create(name=name, upload=request.build_absolute_uri(settings.MEDIA_URL+name))
        f.save()
        serializer = fileSerializer(f)

        SaveFileThread(path, uploaded_file)
        upload2driveThread(name, path, f)

        
        self.response = serializer.data

    def get_response_data(self, chunked_upload, request):
        return self.response
