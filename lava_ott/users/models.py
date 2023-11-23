from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    mobile_number = models.CharField(max_length=25, unique=True)
    is_subscriber = models.BooleanField(default=False)
    image = models.ImageField(upload_to='user_image/', blank=True, null=True)
