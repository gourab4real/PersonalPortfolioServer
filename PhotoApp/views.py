from django.views.generic import detail
from rest_framework import status
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Photo
from .serializers import PhotoSerializer
from rest_framework.parsers import MultiPartParser, FormParser
import urllib3

# Suppress SSL insecure warnings in dev console
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    parser_classes = (MultiPartParser, FormParser)

    # Custom action for GET http://127.0.0.1:8000/photoapp/api/photos/get_all_photos/
    @action(detail=False, methods=['get'])
    def get_all_photos(self, request):
        try:
            photos = Photo.objects.all()
            photos_serialized = self.get_serializer(photos, many=True)
            return Response({'status': 1, 'photos': photos_serialized.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': -1, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Custom action for POST http://127.0.0.1:8000/photoapp/api/photos/add_photo/
    @action(detail=False, methods=['post'])
    def add_photo(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'status': 1, 'message': 'Photo added successfully', 'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response({'status': -1, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def get_photo_by_id(self, request):
        try:
            photo = Photo.objects.get(id=request.data['id'])
            photo_serialized = self.get_serializer(photo)
            return Response({'status': 1, 'photo': photo_serialized.data}, status=status.HTTP_200_OK)
        except Photo.DoesNotExist:
            return Response({'status': -2, 'error': 'Photo not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status': -1, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def delete_photo_by_id(self, request):
        try:
            photo = Photo.objects.get(id=request.data['id'])
            photo.delete()
            return Response({'status': 1, 'message': 'Photo deleted successfully'}, status=status.HTTP_200_OK)
        except Photo.DoesNotExist:
            return Response({'status': -2, 'error': 'Photo not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status': -1, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def update_photo_by_id(self, request):
        try:
            photo = Photo.objects.get(id=request.data['id'])
            if photo.title:
                photo.title = request.data['title']
            if photo.description:
                photo.description = request.data['description']
            photo.save()
            return Response({'status': 1, 'message': 'Photo updated successfully', 'data': self.get_serializer(photo).data}, status=status.HTTP_200_OK)
        except Photo.DoesNotExist:
            return Response({'status': -2, 'error': 'Photo not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status': -1, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)