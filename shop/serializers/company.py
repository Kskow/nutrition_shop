from rest_framework import serializers
from shop.models.company import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("id", "name", "description")
