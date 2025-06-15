from rest_framework import serializers
from .models import PhotoModel
from django.contrib.auth.models import User


class PhotoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoModel
        fields = ['photo']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password','email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            password = validated_data['password'],
            email = validated_data['email']
        )
        user.save()
        return user
    
class GetPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoModel
        fields = '__all__'