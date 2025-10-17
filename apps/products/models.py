from django.db import models

class Product(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    image_list = models.JSONField(default=list, blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    brand = models.CharField(max_length=255, null=True, blank=True)
    stars = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    likes = models.PositiveIntegerField(default=0)
    total_sales = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    small_description = models.CharField(max_length=255, null=True, blank=True)
    long_description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        db_table = 'product'
        
        
