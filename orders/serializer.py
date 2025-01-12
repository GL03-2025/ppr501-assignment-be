from rest_framework import serializers
from accounts.models import AccountDetail
from .models import Order

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