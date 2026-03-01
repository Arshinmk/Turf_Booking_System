from django.db import models
from AdminApp.models import User
from Owner_App.models import TurfDb


class BookingDb(models.Model):

    BOOKING_TYPE = [
        ('Online', 'Online'),
        ('Offline', 'Offline'),
    ]

    turf = models.ForeignKey(TurfDb, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_phone = models.CharField(max_length=15, null=True, blank=True)
    booking_date = models.DateField()
    slot = models.CharField(max_length=50)
    customer_name = models.CharField(max_length=100, null=True, blank=True)
    booking_type = models.CharField(max_length=10, choices=BOOKING_TYPE, default='Online')
    total_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('turf', 'booking_date', 'slot')

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class TurfOwnerApplication(models.Model):
    username =models.CharField(max_length=150)
    owner_name = models.CharField(max_length=150)
    owner_email = models.EmailField()
    owner_phone = models.CharField(max_length=15)
    turf_name = models.CharField(max_length=150)
    turf_city = models.CharField(max_length=100)
    turf_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)