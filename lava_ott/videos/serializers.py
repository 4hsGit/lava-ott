from rest_framework import serializers
from .models import Carousel, SubscriptionPlan, Video, Order


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
            'id',
            'name',
            'description',
            'thumbnail',
            # 'trailer',
            # 'file',
            'director',
            'cast',
            'watch_count',
            'view_on_app',
            'watch_hours',
            # 'duration',
            # 'delete_flag',
            # 'created_at',
            # 'created_by'
        )


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'subscription_amount',
            'subscription_period',
        )


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id',
            'subscription_amount',
            'subscription_period',
            'status',
            'created_at',
            'start_date',
            'expiration_date',
            'is_active'
        )



