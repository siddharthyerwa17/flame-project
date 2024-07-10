from django.db import models

# Create your models here.

from django.db import models
import uuid
# Create your models here.
class Shape_File(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True)
    year = models.IntegerField()
    place_city = models.CharField(max_length=250, blank=True, default='null', null=True)
    shape_file = models.CharField(max_length=250, blank=True, default='null', null=True)
    is_uploaded = models.BooleanField(default=False)   
    
    class Meta:
        verbose_name = "pub_shp_file_info"


class Feedback(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=500, blank=True, default='null', null=True)
    email_id = models.CharField(max_length=100,default='null', null=True) 
    name = models.CharField(max_length=100,default='null', null=True)    
 
    class Meta:
        verbose_name = "feedback"

