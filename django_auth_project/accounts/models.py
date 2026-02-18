from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    name= models.CharField(blank=False, max_length=100, null=False)
    bio = models.TextField(blank=True, null=True)
    phone_number= models.CharField(max_length=11, unique=True, null=True, blank=True)