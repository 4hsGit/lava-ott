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


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = (
            'name',
            'description',
            'thumbnail',
            'trailer',
            'file',
            'director',
            'cast'
        )
