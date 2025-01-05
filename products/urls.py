from django.urls import path
from products.views import ProductList, ProductDetail
# from books.views import get_book
urlpatterns = [
    path('', ProductList.as_view()),
    path('<int:pk>', ProductDetail.as_view())
    # path('', get_book)
]
