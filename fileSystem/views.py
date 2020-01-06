from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
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

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from .models import file

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = file(file_field=request.FILES['file'])
            instance.save()
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


class showFlie(APIView):
    
    def get(self, request):
        File = fileSerializer().Meta.model
        print(request.headers)
        content = {
            'file': self.getFileUrl(File),
            'typ': File.types
            
        }

        
    def getFileUrl(self,File):
        l=[]
        for f in File:
            l.append(f.GetUrl(f))
        return l
            
        return Response(content)

