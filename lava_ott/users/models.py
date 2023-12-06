from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('T', 'Transgender'), ('O', 'Others')]

    mobile_number = models.CharField(max_length=25, unique=True)

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField(blank=True, null=True)

    is_subscriber = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    image = models.ImageField(upload_to='user_image/', blank=True, null=True)

    def has_subscription(self):
        from videos.utils import subscription_exists
        return subscription_exists(self)

    def get_active_subscription(self):
        from videos.utils import get_order
        from videos.models import Order
        from django.core.exceptions import MultipleObjectsReturned
        try:
            order = Order.objects.get(user=self, status='completed', is_active=True, expiration_date__gt=timezone.now())
            order = get_order(order)
        except Order.DoesNotExist:
            order = {}
        except Order.MultipleObjectsReturned:
            raise MultipleObjectsReturned

        return order
