from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group



admin.site.register(models.CreateProject)




