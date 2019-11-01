from rest_framework import serializers
from shop.models.category import Category
from shop.models.company import Company
from shop.models.product import Product


class ProductSerializer(serializers.ModelSerializer):
    reviews = serializers.StringRelatedField(many=True)
    category = serializers.SlugRelatedField(slug_field="name", queryset=Category.objects.all())
    company = serializers.SlugRelatedField(slug_field="name", queryset=Company.objects.all())

    class Meta:
        model = Product
        fields = (
            "name",
            "description",
            "category",
            "company",
            "normal_price",
            "is_promoted",
            "promotion_price",
            "reviews",
            "quantity_in_stock",
            "is_in_stock",
        )
