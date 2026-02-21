from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('owner', 'Owner'),
        ('admin', 'Admin')
    ]

    phone_number = models.CharField(max_length=15,null=True,blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class CategoryDb(models.Model):
    Sport_name=models.CharField(max_length=100)
    Sport_description=models.CharField(max_length=400)
    Sport_img1=models.ImageField(upload_to="Category_image")
    Sport_img2=models.ImageField(upload_to="Category_image")

class CityDb(models.Model):
    Cityname=models.CharField(max_length=100)

