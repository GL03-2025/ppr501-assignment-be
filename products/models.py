from django.db import models
from django.utils.text import slugify

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # img_url = models.CharField(blank=True)
    description = models.TextField(blank=True)

    # Slug 
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    # # Relations
    # category = models.OneToOneField('categories.Category', on_delete=models.CASCADE,blank=True)
    # Relations: Một Category có nhiều Product
    category = models.ForeignKey('categories.Category', on_delete=models.CASCADE, related_name='products', blank=True, null=True)
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    def save(self, *args, **kwargs):
        # Auto-generate slug from name if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at'] 

class Image(models.Model):
    image = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f"{self.product.name} - {self.image}"

    class Meta:
        ordering = ['-created_at']