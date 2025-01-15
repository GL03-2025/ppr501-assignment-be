from rest_framework import serializers
from .models import Cart, CartItem
from accounts.models import AccountDetail
from accounts.serializer import AccountDetailSerializer
from products.models import Product
from products.serializers import GetProductSerializer2

class CartItemSerializer(serializers.ModelSerializer):
    product_detail = serializers.SerializerMethodField()
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_detail', 'quantity', 'created_at', 'updated_at']

    def get_product_detail(self, obj):
        return GetProductSerializer2(obj.product).data

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    account_detail = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'account_detail', 'items', 'created_at', 'updated_at']

    def get_account_detail(self, obj):
        account_detail = AccountDetail.objects.get(user=obj.user)
        return AccountDetailSerializer(account_detail).data