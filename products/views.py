from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status, viewsets, generics
from django.shortcuts import get_object_or_404

from accounts.serializer import CustomPagination
from .models import Product
from .serializers import  GetProductSerializer, ProductFilter, SetProductSerializer


# Create your views here.

# class ProductList(APIView):
#     def get(self, request):
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     def get(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#
#     def patch(self, request, pk):
#         """Update partial fields of a product"""
#         product = get_object_or_404(Product, pk=pk)
#         serializer = ProductSerializer(product, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         """Delete a product"""
#         product = get_object_or_404(Product, pk=pk)
#         product.delete()
#         return Response({"message": "Product deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
class ProductListView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = GetProductSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    # permission_classes = [IsAuthenticated]  # Phân quyền

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = GetProductSerializer

class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = SetProductSerializer