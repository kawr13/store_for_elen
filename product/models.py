from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    phone_number = models.CharField(max_length=20)
    avatar = models.ImageField(upload_to='users_avatars', blank=True)