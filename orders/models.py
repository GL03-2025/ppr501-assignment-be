import uuid
from enum import Enum
from django.db import models
from accounts.models import AccountDetail

class OrderStatus(Enum):
    UNPAID = 'unpaid'
    FAILED = 'failed'
    PAID = 'paid'

    @classmethod
    def choices(cls):
        return [(tag.value, tag.name.replace('_', ' ').capitalize()) for tag in cls]

class TransactionMethod(Enum):
    VNPAY = 'vnpay'
    CASH = 'cash'
    NOPAY = 'nopay'

    @classmethod
    def choices(cls):
        return [(tag.value, tag.name.replace('_', ' ').capitalize()) for tag in cls]

class Order(models.Model):
    accountId = models.ForeignKey(AccountDetail, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=100, choices=OrderStatus.choices(), default=OrderStatus.UNPAID.value)
    description = models.TextField()
    content = models.TextField()
    notes = models.TextField()
    address = models.CharField(null=True,max_length=400)
    method = models.CharField(
        max_length=100, choices=TransactionMethod.choices(), default=TransactionMethod.NOPAY.value)
    payment_url = models.CharField(max_length=700, null=True, blank=True)
    redirect_url = models.URLField(null=True, blank=True)
    order_uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    def __str__(self):
        return f"Order {self.id} - {self.status}"

class OrderDetail(models.Model):
    orderId = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details' ) # related_name để truy xuất từ Order
    productId = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.orderId.id} - {self.productId.name} - {self.quantity} - {self.price}"