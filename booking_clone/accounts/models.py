from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class HotelUser(User):
    profile_picture = models.ImageField(upload_to="profile")
    phone_number = models.IntegerField()
    