"""
URL configuration for lava_ott project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

url_prefix = 'api/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{url_prefix}users/', include('users.urls')),
    path(f'{url_prefix}videos/', include('videos.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.http import Http404


def handler404(request, exception):
    raise Http404


urlpatterns += [
    # Include the 404 handler at the end
    handler404,
]
