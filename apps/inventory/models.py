from django.db import models
from apps.products.models import Product
from apps.accounts.models import User
from django.core.validators import MinValueValidator


class Store(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'store'
        verbose_name = "Store"
        verbose_name_plural = "Stores"

class Warehouse(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='warehouses')
    name = models.CharField(max_length=255)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.store.name}"

    class Meta:
        verbose_name = "Warehouse"
        verbose_name_plural = "Warehouses"
        db_table = 'warehouse'

class Stock(models.Model):
    code = models.CharField(max_length=100, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stocks')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stocks')
    cant = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    threshold = models.SmallIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.product.name}"

    class Meta:
        db_table = 'stock'
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
        unique_together = ['product', 'warehouse']
        

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
    
    
class StockMovement(models.Model):
    ACTION_OPERATION_CHOICES  = (
        ('1', 'salida'),
        ('2', 'entrada'),   
    )
    ACTION_TYPE_CHOICES  = (
        ('1', 'simple'),
        ('2', 'multiple'),  
    )
    action_operation = models.CharField(max_length=1, choices=ACTION_OPERATION_CHOICES, default='2') 
    action_type = models.CharField(max_length=1, choices=ACTION_TYPE_CHOICES, default='1') 
    created_date = models.DateTimeField(auto_now_add=True)
    motive = models.CharField(max_length=80) 
    description = models.TextField(null=True, blank=True)
    cant = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False,blank=False, related_name='user_stock_movement')
    stock_one=models.ForeignKey(Stock, on_delete=models.CASCADE, null=False,blank=False, related_name='stock_one_movement')
    stock_two=models.ForeignKey(Stock, on_delete=models.CASCADE, null=True,blank=True, related_name='stock_two_movement')
    
    
    class Meta:
        verbose_name = "Stock movement"
        verbose_name_plural = "Stocks Movements"

    def __str__(self):
        return f'{self.pk}'
    
class Income(models.Model):
    created_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="created_user")
    created_date = models.DateTimeField(auto_now_add=True,editable=False)
    motive = models.CharField(max_length=80) 
    description = models.TextField(null=True,blank=True)
    amount = models.DecimalField(max_digits=12, default=0, decimal_places=2,validators=[MinValueValidator(0.01)])
    
    class Meta:
        verbose_name = "Income"
        verbose_name_plural = "Incomes"

    def __str__(self):
        return f"{self.pk}"

class Outcome(models.Model):
    created_user=models.ForeignKey(User, on_delete = models.CASCADE, verbose_name="created_user")
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    motive = models.CharField(max_length=80) 
    description = models.TextField(null=True, blank=True)
    amount = models.DecimalField(max_digits=12, default=0, decimal_places=2, validators=[MinValueValidator(0.01)])
    
    class Meta:
        verbose_name = "Spent"
        verbose_name_plural = "Spents"

    def __str__(self):
        return f"{self.pk}"