from django.urls import path
from .views import *

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Carousel
    path('carousel-create/', carousel_create, name='carousel-create'),
    path('carousel-list/', carousel_list, name='carousel-list'),
]
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
