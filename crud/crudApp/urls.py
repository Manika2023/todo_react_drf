from django.urls import path,include
from . import views
urlpatterns = [
path('api/products/',views.Product_list_api,name="products_list"),
path('api/products/create/',views.product_create_api,name="product_create"),
path('api/products/<int:id>/',views.product_detail_api,name="product_detail"),
path('api/products/update/<int:id>/',views.product_update_api,name="product_update"),
path('api/products/delete/<int:id>/',views.product_delete_api,name="product_delete"),
path('search/',views.search_api,name="search")

]
