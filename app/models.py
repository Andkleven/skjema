from django.db import models
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator 
from itertools import chain
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms
from decimal import Decimal
from PIL import Image
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class CreateProject(models.Model):
    data                                        = models.TextField()

