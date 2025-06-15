from django.shortcuts import render
from rest_framework import viewsets, mixins
from .models import PhotoModel
from .serializer import PhotoModelSerializer, RegisterSerializer, GetPhotoSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
import os
from PIL import Image
from PIL.ExifTags import TAGS
import datetime
from loguru import logger
from django.utils import timezone
from django.db.models.functions import TruncMonth 
from collections import defaultdict
# Create your views here.
class PhotoModelViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def create(self, request):
        if(request.FILES.get('photo') is None):
            return Response({'error': 'Some error occurred in uploading image'}, status=status.HTTP_204_NO_CONTENT)
        else:
            try:
                photo_file = request.FILES.get('photo')
                captured_on = None
                timedata = None 
                try:
                    image = Image.open(photo_file)
                    exif_data = image._getexif()
                    if exif_data:
                        for tag_id, value in exif_data.items():
                            tag = TAGS.get(tag_id, tag_id)
                            if tag == 'DateTimeOriginal':
                                captured_on = datetime.datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                                logger.info(f"Captured : {captured_on}")
                                timedata = timezone.make_aware(captured_on, timezone.get_current_timezone())
                                captured_on = timedata
                                logger.info(f'Image upload {timedata}')
                                break
                except Exception:
                    captured_on = None
                logger.info(f'Image upload {timedata}')
                photo = PhotoModel.objects.create(
                    uploaded_by=self.request.user,
                    photo=photo_file,
                    captured_on=captured_on
                )
                photo.save()
                return Response({'message':'Photos have been uploaded'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error':f'{str(e)}'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    def list(self, request):
        photos = request.user.photos.annotate(month=TruncMonth('captured_on')).order_by('-captured_on')

        grouped_photos = defaultdict(list)
        for photo in photos:
            key = photo.month.strftime('%Y-%m') if photo.month is not None else 'Undated'
            serializer = GetPhotoSerializer(photo)
            grouped_photos[key].append(serializer.data)

        # Convert dict to list of {date: ..., photos: [...]}
        response_data = []
        for date, photos_list in grouped_photos.items():
            response_data.append({
                'date': date,
                'photos': photos_list
            })

        return Response(response_data)
    def destroy(self, request, pk = None):
        if pk is not None:
            try:
                photo = PhotoModel.objects.get(pk = pk)
                photo_path = photo.photo.path
                os.remove(photo_path)
                photo.delete()
                return Response({'message':'Image deleted'}, status = status.HTTP_200_OK)
            
            except Exception as e:
                return Response({'error':"Photo doesn't exist"}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error':'Not a valid Image to delete'}, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(viewsets.ViewSet):
    @permission_classes([AllowAny])
    def create(self, request):
        serializer = RegisterSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'User has been created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    @permission_classes([IsAuthenticated])
    def destroy(self,request, pk=None):
        try:
            user = self.request.user
            user.delete()
            return Response({'error':'Account Removed'}, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status = status.HTTP_400_BAD_REQUEST)
    @action(methods=['GET'],detail=False, url_name="session", permission_classes = [IsAuthenticated])
    def check_session(self,request):
        return Response({'message':'Valid token'},status = status.HTTP_200_OK)