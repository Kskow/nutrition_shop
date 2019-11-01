from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from shop.models.product import Product


class Review(models.Model):
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    rate = models.IntegerField(blank=False, validators=[MinValueValidator(1), MaxValueValidator(5)])
    opinion = models.TextField(blank=False)
    product = models.ForeignKey(Product, related_name="reviews", on_delete=models.CASCADE, blank=False)

    def __str__(self) -> str:
        return f"{self.user}, {self.opinion}, {self.rate}"
