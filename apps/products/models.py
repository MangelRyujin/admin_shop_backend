from django.db import models
from django.core.validators import MinValueValidator

class Product(models.Model):
    code = models.CharField(max_length=100, unique=True)
    # slug = models.CharField(max_length=255, unique=True)
    # unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
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

class BulkPricing(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='offerts')
    cant = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    
    class Meta:
        verbose_name = "Offert"
        verbose_name_plural = "Offerts"

    def __str__(self):
        return f"{self.product.name} - cant {self.cant} for {self.total_price}"   
        
class Offert(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='offerts')
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    init_date = models.DateField(auto_now=False,auto_now_add=False)
    end_date = models.DateField(auto_now=False,auto_now_add=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Offert"
        verbose_name_plural = "Offerts"

    def __str__(self):
        return self.name