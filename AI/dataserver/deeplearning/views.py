from multiprocessing import Process

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializer import FileSerializer, TrainModelSerializer
from .models import File, TrainedModel
from .train_with_azure import train

class FileViewSet(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    
    queryset = File.objects.all()
    serializer_class = FileSerializer
    
    def create(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return Response({'message': 'token is needed'}, status=status.HTTP_401_UNAUTHORIZED)
            
        return super(FileViewSet, self).create(request, *args, **kwargs)
        

    
class TrainViewSet(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    
    queryset = File.objects.all()
    serializer_class = FileSerializer
    
    
    def retrieve(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return Response({'message': 'token is needed'}, status=status.HTTP_401_UNAUTHORIZED)
        
        file = self.get_queryset().latest('upload_at')
        serializer = self.get_serializer(file)
        
        p = Process(target=train, args=(serializer.data['file'], 1, ))
        p.start()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class TrainModelViewSet(viewsets.ModelViewSet):
    queryset = TrainedModel.objects.all()
    serializer_class = TrainModelSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_queryset().latest('version')
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
        