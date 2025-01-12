from enum import Enum
from django.db import models
from accounts.models import AccountDetail

class OrderStatus(Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'

    @classmethod
    def choices(cls):
        return [(tag.value, tag.name) for tag in cls]

class Order(models.Model):
    accountId = models.ForeignKey(AccountDetail, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='active')
    description = models.TextField()
    content = models.TextField()
    notes = models.TextField()
    method = models.CharField(max_length=50)

    def __str__(self):
        return f"Order {self.id} - {self.status}"