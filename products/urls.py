from django.urls import path

from products.views import (ProductListView, ProductCreateView, ProductDetailView)

# from products.views import ProductList, ProductDetail
# from books.views import get_book
urlpatterns = [
    # path('', ProductList.as_view()),
    # path('<int:pk>', ProductDetail.as_view())
    # path('', get_book)

    path('manage-products/', ProductListView.as_view({'get': 'list'}), name='manage-products'),
    path('manage-product/', ProductCreateView.as_view(), name='product-create'),
    path('manage-product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]
