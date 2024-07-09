from django.contrib import admin

from .models import User
from .models import Project


admin.site.register(User)
admin.site.register(Project)
