from django.contrib.auth.models import User
from django.db import models


class Cart(models.Model):
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, blank=False)
    last_update = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False, blank=False)
