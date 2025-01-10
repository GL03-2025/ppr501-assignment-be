from rest_framework import serializers

from products.serializers import GetProductTmpSerializer
from .models import Category

from django_filters import rest_framework as filters

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


# map dữ liệu từ model sang json
class GetCategorySerializer(serializers.ModelSerializer):
    products = GetProductTmpSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = '__all__'
        depth = 1

class SetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug']

class CategoryFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Category
        fields = ['name']