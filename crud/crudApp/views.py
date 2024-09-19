from django.shortcuts import render
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Product_Category
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated,AllowAny

# Create your views here.
@api_view(['POST'])
# all user can  see even who is not authenticated
@permission_classes([AllowAny])
def Product_list_api(request):
     if request.method == 'POST':
          products=Product_Category.objects.all()
          serializer=ProductSerializer(products,many=True)
          return Response({"message":"product retrieved successfully!","data":serializer.data},status=status.HTTP_200_OK)
     else:
          return Response({"error":"Failed to retrieved successfully"},status=status.HTTP_400_BAD_REQUEST)     
     
@api_view(['POST'])     
@permission_classes([IsAuthenticated])
def product_create_api(request):
     if request.method == 'POST':
          serializer=ProductSerializer(data=request.data)
          if serializer.is_valid():
               serializer.save()
               return Response({"message":"post created successfully","data":serializer.data},status=status.HTTP_201_CREATED)
          else:
               print(serializer.error_messages)
               return Response({"error":"Failed to create post, please try again","data":serializer.errors},status=status.HTTP_400_BAD_REQUEST) 


# view for retrieving one product detail
@api_view(['POST'])
@permission_classes([AllowAny])
def product_detail_api(request,id):
     try:
          product=Product_Category.objects.get(pk=id)
     except Product_Category.DoesNotExist:
          return Response({"error":"Product not found"},status=status.HTTP_400_BAD_REQUEST)     
     if request.method == "POST":
          serializer=ProductSerializer(product) 
          return Response({"message":"product retrieved successfully! ","data":serializer.data},status=status.HTTP_200_OK)
     else:
          return  Response({"error":"Failed to  retrieved the  product !","data":serializer.errors},status=status.HTTP_200_OK)



# View to retrieve product details
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def product_detail_api(request, id):
#     try:
#         product = Product_Category.objects.get(pk=id)
#         print("product code is ",product.product_code)
#     except Product_Category.DoesNotExist:
#         return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    
#     serializer = ProductSerializer(product)
#     return Response(serializer.data, status=status.HTTP_200_OK)

# View to update product details
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def product_update_api(request, id):
    try:
        product = Product_Category.objects.get(pk=id)
    except Product_Category.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Product updated successfully!", "data": serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Failed to update the product!", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def product_delete_api(request,id):
     try:
          product=Product_Category.objects.get(pk=id)
     except Product_Category.DoesNotExist:
          return Response({"error":"Product not found"},status=status.HTTP_400_BAD_REQUEST)     
     
     product.delete()
     return Response({"message":"Product deleted successfully!"},status=status.HTTP_204_NO_CONTENT)

     
@api_view(['GET'])
def search_api(request):
    productName = request.GET.get('name')
    
    if productName:
        try:
            # Filter products by name
            posts = Product_Category.objects.filter(name__icontains=productName)
            serializer = ProductSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            # Log the exception and return a server error response
            print(f'Error: {e}')
            return Response({'error': 'An error occurred while processing your request.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'error': 'Name parameter is missing'}, status=status.HTTP_400_BAD_REQUEST)