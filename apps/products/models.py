from django.db import models
from django.core.validators import MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(
        upload_to='categories/',
        null=True, 
        blank=True,
        help_text="Imagen representativa de la categoría"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'category'
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def subcategories_count(self):
        return self.subcategories.filter(is_active=True).count()

    @property
    def products_count(self):
        """Cantidad total de productos en esta categoría (incluyendo subcategorías)"""
        from django.db.models import Count
        return Product.objects.filter(
            models.Q(category=self) | models.Q(subcategory__category=self),
            is_active=True,
            is_deleted=False
        ).distinct().count()

class SubCategory(models.Model):
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='subcategories'
    )
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "SubCategory"
        verbose_name_plural = "SubCategories"
        ordering = ['name']
        unique_together = ['category', 'name']  # Nombre único por categoría

    def __str__(self):
        return f"{self.category.name} → {self.name}"

    @property
    def products_count(self):
        """Cantidad de productos en esta subcategoría"""
        return self.products.filter(is_active=True, is_deleted=False).count()

class Product(models.Model):
    code = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=255, unique=True, default='N/A')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.01, validators=[MinValueValidator(0.01)])
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
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"{self.code} - {self.name}"

class BulkPricing(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bulk_pricings')
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
    