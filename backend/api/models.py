from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class PhotoModel(models.Model):
    uploaded_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='photos')
    photo = models.FileField(upload_to='media')
    uploaded_on = models.DateTimeField(auto_now=True)
    category = models.CharField(null=True, max_length=20)
    captured_on = models.DateTimeField(null=True)