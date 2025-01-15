from django.db import models

class BaseEntity(models.Model):
    createBy = models.CharField(max_length=255)
    createAt = models.DateTimeField(auto_now_add=True)
    updateBy = models.CharField(max_length=255, null=True, blank=True)
    updateAt = models.DateTimeField(auto_now=True)
    deleteBy = models.CharField(max_length=255, null=True, blank=True)
    deleteAt = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True