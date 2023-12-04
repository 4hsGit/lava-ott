from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


class Video(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    thumbnail = models.ImageField(upload_to='thumbnails/')
    trailer = models.FileField(upload_to='trailers')
    file = models.FileField(upload_to='videos')

    director = models.CharField(max_length=100)
    cast = models.TextField()

    watch_count = models.PositiveIntegerField(default=0)
    view_on_app = models.BooleanField(default=False)
    watch_hours = models.FloatField(default=0)
    duration = models.FloatField(blank=True, null=True)
    delete_flag = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)


class Order(models.Model):
    STATUS_CHOICES = [('pending', 'pending'), ('completed', 'completed')]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    subscription_amount = models.FloatField()
    subscription_period = models.CharField(max_length=10)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    created_at = models.DateTimeField(default=timezone.now)

    start_date = models.DateTimeField()
    expiration_date = models.DateTimeField()
    is_active = models.BooleanField(default=False)


class SubscriptionPlan(models.Model):
    SUB_PERIOD_CHOICES = [('month', 'month'), ('year', 'year')]

    subscription_amount = models.FloatField()
    subscription_period = models.CharField(max_length=10, choices=SUB_PERIOD_CHOICES)


class Carousel(models.Model):
    image = models.ImageField(upload_to='carousel')
