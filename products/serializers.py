from rest_framework import serializers
from .models import Product
from categories.models import Category

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category', 'img_url']

    def create(self, validated_data):
        # Category is already resolved to an instance by PrimaryKeyRelatedField
        category = validated_data.pop('category')
        product = Product.objects.create(category=category, **validated_data)
        return product