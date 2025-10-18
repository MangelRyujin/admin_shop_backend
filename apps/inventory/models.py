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
    cant = models.PositiveIntegerField(default=0) # add min value validator (1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2) # add min value validator (0.01)
    is_active = models.BooleanField(default=True)
    expire_date = models.DateField(null=True, blank=True)
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
    # created_at = models.DateTimeField(auto_now_add=True) # change actual created_date for this field
    motive = models.CharField(max_length=80) 
    description = models.TextField(null=True, blank=True)
    # motive = models.TextField(null=True, blank=True)  # change actual motive and description for this field
    cant = models.PositiveIntegerField(validators=[MinValueValidator(1)]) # remove validation of serializer
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False,blank=False, related_name='user_stock_movement') # remove
    # create_by_user_id = models.IntegerField(null=True, blank=True)
    # create_by_user_full_name = models.CharField(max_length=150, null=True, blank=True)
    stock_one=models.ForeignKey(Stock, on_delete=models.CASCADE, null=False,blank=False, related_name='stock_one_movement') # remove
    stock_two=models.ForeignKey(Stock, on_delete=models.CASCADE, null=True,blank=True, related_name='stock_two_movement') # remove
    # Remove relations for stock_one and stock_two
    # stock_from_id = models.IntegerField(null=True, blank=True)
    # stock_from_code = models.CharField(max_length=100, null=True, blank=True)
    # stock_from_product_id = models.IntegerField(null=True, blank=True)
    # stock_from_product_name = models.CharField(max_length=150, null=True, blank=True)
    # stock_from_wharehouse_id = models.IntegerField(null=True, blank=True)
    # stock_from_wharehouse_name = models.IntegerField(null=True, blank=True)
    # stock_from_prev_cant = models.PositiveIntegerField(null=True, blank=True)
    # stock_from_new_cant = models.PositiveIntegerField(null=True, blank=True)
    # stock_to_id = models.IntegerField(null=True, blank=True)
    # stock_to_code = models.CharField(max_length=100, null=True, blank=True)
    # stock_to_product_id = models.IntegerField(null=True, blank=True)
    # stock_to_product_name = models.CharField(max_length=150, null=True, blank=True)
    # stock_to_wharehouse_id = models.IntegerField(null=True, blank=True)
    # stock_to_wharehouse_name = models.IntegerField(null=True, blank=True)
    # stock_to_prev_cant = models.PositiveIntegerField(null=True, blank=True)
    # stock_to_new_cant = models.PositiveIntegerField(null=True, blank=True)
    
    
    class Meta:
        verbose_name = "Stock movement"
        verbose_name_plural = "Stocks Movements"

    def __str__(self):
        return f'{self.pk}'
    
class Income(models.Model): # Remove this class
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

class Outcome(models.Model): # Remove this class
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