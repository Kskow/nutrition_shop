from django.core.validators import MinValueValidator
from django.db import models
from shop.models.category import Category
from shop.models.company import Company


class Product(models.Model):
    name = models.CharField(max_length=30, blank=False, unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=False)
    normal_price = models.DecimalField(max_digits=5, decimal_places=2, blank=False)
    is_promoted = models.BooleanField(default=False)
    promotion_price = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    quantity_in_stock = models.IntegerField(blank=False, validators=[MinValueValidator(1)])
    is_in_stock = models.BooleanField(blank=False, default=True)

    def __str__(self) -> str:
        if self.is_promoted:
            return f"{self.name}, {self.normal_price}, {self.promotion_price}"
        return f"{self.name}, {self.normal_price}"
