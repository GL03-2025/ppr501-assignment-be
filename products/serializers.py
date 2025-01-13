from rest_framework import serializers
from .models import Product, Image
from django_filters import rest_framework as filters


class GetImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id','image','created_at']

class GetProductTmpSerializer(serializers.ModelSerializer):
    images = GetImagesSerializer(many=True)
    is_deleted = serializers.BooleanField(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'
        # depth = 1  # Để hiển thị các trường của category
        # fields = ['id', 'name', 'price', 'description', 'slug', 'created_at', 'is_active','images']

class GetProductSerializer(serializers.ModelSerializer):
    images = GetImagesSerializer(many=True)
    is_deleted = serializers.BooleanField(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'
        depth = 1

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if images_data is not None:
            # xóa hết tất cả ảnh trước khi thêm ảnh mới
            instance.images.all().delete()
            for image_data in images_data:
                Image.objects.create(product=instance, **image_data)
        return instance

class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    slug = filters.CharFilter(field_name='slug', lookup_expr='icontains')
    is_deleted = filters.BooleanFilter(field_name='is_deleted')
    class Meta:
        model = Product
        fields = ['slug','name','is_deleted']

class CustomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image']

class SetProductSerializer(serializers.ModelSerializer):
    images = CustomImageSerializer(many=True, write_only =True )
    is_deleted = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'
        # exclude = ['is_deleted']
    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        # ** Nó sẽ lỗi dữ liệu từ dictionary thành các tham số với keyword arguments
        # ví dụ {'name': 'product1', 'price': 1000, 'category': <Category: Category object (1)>}
        # sẽ trở thành name='product1', price=1000, category=<Category: Category object (1)>
        product = Product.objects.create(**validated_data) # Dùng ** để unpack dữ liệu còn lại
        for image_data in images_data:
            Image.objects.create(product=product, **image_data)
        return product