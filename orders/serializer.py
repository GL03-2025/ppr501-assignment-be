from rest_framework import serializers
from accounts.models import AccountDetail
from products.serializers import GetProductSerializer
from .models import Order, OrderDetail, TransactionMethod, OrderStatus
from django_filters import rest_framework as filters

from .utils import Util


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
        #fields = ['id', 'accountDetail', 'amount', 'status', 'description', 'content', 'notes', 'method']
        fields = ['id', 'accountDetail', 'amount', 'description', 'content', 'notes' ]

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
        read_only_fields = ['payment_url', 'order_uuid', 'status']
    def create(self, validated_data):
        order_details_data = validated_data.pop('order_details')
        order = Order.objects.create(**validated_data)
        for order_detail_data in order_details_data:
            order_detail_data['orderId'] = order
            OrderDetail.objects.create(**order_detail_data)
        if order.method == TransactionMethod.VNPAY.value:
            try:
                request = self.context.get('request')
                payment_url = Util.post_payment(order, request)
                order.payment_url = payment_url
                order.status = OrderStatus.FAILED.value
            except Exception as e:
                raise serializers.ValidationError({"error": f"Failed to process VNPAY payment: {str(e)}"})
        elif order.method == TransactionMethod.CASH.value:
            order.status = OrderStatus.PAID.value
        else:
            order.status = OrderStatus.FAILED.value
        order.save()
        return order

class OrderFilter(filters.FilterSet):
    min_amount = filters.NumberFilter(field_name='amount', lookup_expr='gte', label='Minimum amount')
    max_amount = filters.NumberFilter(field_name='amount', lookup_expr='lte', label='Maximum amount')
    content = filters.CharFilter(field_name='content', lookup_expr='icontains', label='Content contains')
    status = filters.ChoiceFilter(field_name='status', choices=OrderStatus.choices(), label='Order status')
    method = filters.ChoiceFilter(field_name='method', choices=TransactionMethod.choices(), label='Payment method')
    class Meta:
        model = Order
        fields = ['amount', 'content', 'status', 'method']