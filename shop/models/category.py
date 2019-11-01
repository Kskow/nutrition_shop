from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=30, blank=False, unique=True)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.name}"
