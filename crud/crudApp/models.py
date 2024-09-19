
from django.db import models

# Create your models here.

class Product_Category(models.Model):
    product_code = models.BigIntegerField(default=0)
    name = models.CharField(max_length=100)
    description = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    status = models.CharField(max_length=10, choices=[('Active', 'Active'), ('Inactive', 'Inactive')])

    def __str__(self):
        return self.name

