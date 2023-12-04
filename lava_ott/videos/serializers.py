from rest_framework import serializers
from .models import Carousel, SubscriptionPlan, Video


class CarouselSerializer(serializers.Serializer):
    image = serializers.ListField(child=serializers.ImageField())


class CarouselListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carousel
        fields = ['image']


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = (
            'subscription_amount',
            'subscription_period'
        )


class VideoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = (
            'name',
            'description',
            'thumbnail',
            'trailer',
            'file',
            'director',
            'cast',
            'created_by'
        )


class VideoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = (
            'name',
            'description',
            'thumbnail',
            'trailer',
            'file',
            'director',
            'cast',
            'watch_count',
            'view_on_app',
            'watch_hours',
            'duration',
            'delete_flag',
            'created_at',
            'created_by'
        )
