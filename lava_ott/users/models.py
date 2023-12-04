from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('T', 'Transgender'), ('O', 'Others')]

    mobile_number = models.CharField(max_length=25, unique=True)

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField(blank=True, null=True)

    is_subscriber = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    image = models.ImageField(upload_to='user_image/', blank=True, null=True)
