from enum import Enum

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

class UserStatus(Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    BLOCKED = 'blocked'

    @classmethod
    def choices(cls):
        return [(tag.value, tag.name) for tag in cls]


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    # sử dụng nhanh như này status='active' thay vì như này status=UserStatus.ACTIVE
    status = models.CharField(
        max_length=100, choices=[(tag, tag.value) for tag in UserStatus], default='active')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

class AccountDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    additional_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.email