from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import  viewsets, generics
from rest_framework.permissions import IsAuthenticated

from accounts.serializer import CustomPagination
from .models import Product
from .serializers import  GetProductSerializer, ProductFilter, SetProductSerializer

class ProductListView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = GetProductSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    #permission_classes = [IsAuthenticated]  # Phân quyền

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = GetProductSerializer
    #permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = SetProductSerializer
    #permission_classes = [IsAuthenticated]