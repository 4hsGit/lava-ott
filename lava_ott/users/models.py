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

    # Session
    session_key = models.TextField(blank=True, null=True)
    session_expire_date = models.DateTimeField(blank=True, null=True)

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

    def set_custom_session(self, keep_logged_in=False, admin=False):
        print('keep_logged_in == ', keep_logged_in)
        from .utils import generate_token
        from datetime import timedelta
        if admin is True:
            from django.conf import settings
            expire_period = timedelta(seconds=settings.SESSION_COOKIE_AGE)
        elif keep_logged_in is False:
            expire_period = timedelta(hours=24)
        else:
            expire_period = timedelta(days=30)

        token = generate_token(self)
        self.session_key = token
        self.session_key = token
        self.session_expire_date = timezone.now() + expire_period
        self.save()

        return token
