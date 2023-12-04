from django.urls import path
from .views import *

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Carousel
    path('carousel-create/', carousel_create, name='carousel-create'),
    path('carousel-list/', carousel_list, name='carousel-list'),

    # Subscription Plan
    path('subscription-plan/create/', subscription_plan_create, name='subscription-plan-create'),
    path('subscription-plan/list/', subscription_plan_list, name='subscription-plan-list'),
    path('subscription-plan/delete/', subscription_plan_delete, name='subscription-plan-delete'),

    # Video
    path('video-create/', VideoCreateView.as_view(), name='video-create'),
    path('video-list/', VideoListView.as_view(), name='video-list'),
    path('video-delete/', VideoDeleteView.as_view(), name='video-delete'),
]
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
