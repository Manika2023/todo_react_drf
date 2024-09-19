from rest_framework import serializers
from .models import Product_Category

class ProductSerializer(serializers.ModelSerializer):
     class Meta:
          model = Product_Category
          fields = '__all__'

     def validate_product_code(self, value):
          if    value < 0:
               raise serializers.ValidationError({"error":"product code can not be negative"})
          return value
     
     def validate_price(self, value):
          if value < 0:
               raise serializers.ValidationError({"error":"price can not be the negative"})            
          return value
                    