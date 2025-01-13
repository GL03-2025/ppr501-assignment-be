from rest_framework import serializers
from accounts.models import AccountDetail
from products.serializers import GetProductSerializer
from .models import Order, OrderDetail
from django_filters import rest_framework as filters

class AccountDetailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = AccountDetail
        fields = ['id', 'email']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {
            'accountId': {'required': False}
        }

class CreateOrderResponseSerializer(serializers.ModelSerializer):
    accountDetail = AccountDetailSerializer(source='accountId')

    class Meta:
        model = Order
        fields = ['id', 'accountDetail', 'amount', 'status', 'description', 'content', 'notes', 'method']


class GetOrderDetailSerializer(serializers.ModelSerializer):
    productId = GetProductSerializer() # Lấy từ products.serializers
    class Meta:
        model = OrderDetail
        fields = '__all__'
class GetAllOrderSerializer(serializers.ModelSerializer):
    order_details = GetOrderDetailSerializer(many=True)
    class Meta:
        model = Order
        fields = '__all__'
        depth = 1


class SetOrderDetailSerializer(serializers.ModelSerializer):
    orderId = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = OrderDetail
        fields = '__all__'

class OrderCreateSerializer(serializers.ModelSerializer):
    order_details = SetOrderDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        order_details_data = validated_data.pop('order_details')
        order = Order.objects.create(**validated_data)
        for order_detail_data in order_details_data:
            order_detail_data['orderId'] = order  # Gán orderId cho các chi tiết đơn hàng
            OrderDetail.objects.create(**order_detail_data)
        return order

class OrderFilter(filters.FilterSet):
    min_amount = filters.NumberFilter(field_name='amount', lookup_expr='gte', label='Minimum amount')
    max_amount = filters.NumberFilter(field_name='amount', lookup_expr='lte', label='Maximum amount')
    content = filters.CharFilter(field_name='content', lookup_expr='icontains', label='Content contains')
    status = filters.CharFilter(field_name='status', lookup_expr='iexact', label='Order status')
    class Meta:
        model = Order
        fields = ['amount', 'content', 'status']