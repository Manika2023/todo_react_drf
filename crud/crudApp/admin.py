# Register your models here.
from django.contrib import admin
from .models import Product_Category
# Register your models here.
@admin.register(Product_Category)
class ProductCategoryAdmin(admin.ModelAdmin):
     list_display=['id','product_code','name','description','datetime','price','status']