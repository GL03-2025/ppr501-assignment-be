from rest_framework import serializers
from products.serializers import GetProductTmpSerializer
from .models import Category
from django_filters import rest_framework as filters


# map dữ liệu từ model sang json
class GetCategorySerializer(serializers.ModelSerializer):
    products = GetProductTmpSerializer(many=True, read_only=True)
    is_deleted = serializers.BooleanField(read_only=True)
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
    is_deleted = filters.BooleanFilter(field_name='is_deleted')
    class Meta:
        model = Category
        fields = ['name', 'is_deleted']