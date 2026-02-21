from django.db import models

# Create your models here.
class TurfDb(models.Model):
    Turf_name = models.CharField(max_length=100)
    Sport = models.CharField(max_length=100)
    Owner = models.CharField()
    City = models.CharField()
    Location = models.CharField(max_length=300)
    Price_per_hour = models.IntegerField()
    Description = models.CharField(max_length=400)
    Size = models.CharField(max_length=50)
    Turf_image1 = models.ImageField(upload_to='turfs_image')
    Turf_image2 = models.ImageField(upload_to='turfs_image')