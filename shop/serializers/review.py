from rest_framework import serializers
from shop.models.product import Product
from shop.models.review import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    product = serializers.SlugRelatedField(slug_field="name", queryset=Product.objects.all())

    class Meta:
        model = Review
        fields = ("id", "user", "rate", "opinion", "product")
        validators = [serializers.UniqueTogetherValidator(queryset=model.objects.all(), fields=("user", "product"))]
