from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.permission import canOperatingInfo
from fileSystem.serializers import fileSerializer, typesSerializer
from fileSystem.models import file, types




class fileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = file.objects.all()
    serializer_class = fileSerializer


class typesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = types.objects.all()
    serializer_class = typesSerializer
    
## in work

#from django.http import HttpResponseRedirect
#from django.shortcuts import render
#from .forms import UploadFileForm

#def upload_file(request):
#    if request.method == 'POST':
#        form = UploadFileForm(request.POST, request.FILES)
#        if form.is_valid():
#            instance = file(file_field=request.FILES['file'])
#            instance.save()
#            return HttpResponseRedirect('/success/url/')
#    else:
#        form = UploadFileForm()
#    return render(request, 'upload.html', {'form': form})


        
class GetType(APIView):
    def get(self, request, pk):

        try:
            type = types.objects.get(pk=pk)
        except types.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


        if request.method == 'GET':
            serializer =  typesSerializer(type, context={'request': request})
            return Response(serializer.data)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class GetFile(APIView):
    def get(self, request, pk):

        try:
            files = file.objects.get(pk=pk)
        except file.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


        if request.method == 'GET':
            serializer =  fileSerializer(files, context={'request': request})
            return Response(serializer.data)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class PostFile(APIView):
    def post(self, request):

        file.objects.all()

        if request.method == 'POST':
            serializer =  fileSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

