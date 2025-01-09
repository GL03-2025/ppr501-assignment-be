
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.views import APIView

from accounts.serializer import CustomPagination
from categories.models import Category
from categories.serializers import GetCategorySerializer, SetCategorySerializer, CategoryFilter


# Create your views here.
class Categories(APIView):
    def get(self, request):
        return

class CategoryListView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = GetCategorySerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter
    # permission_classes = [IsAuthenticated]  # Phân quyền

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = GetCategorySerializer

class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = SetCategorySerializer