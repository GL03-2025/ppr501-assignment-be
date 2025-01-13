from django.urls import path
from .views import CartView, CartItemView, CartItemUpdateView, CartItemDeleteView, CheckoutView

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('items/', CartItemView.as_view(), name='cart-items'),
    path('items/<int:pk>/', CartItemUpdateView.as_view(), name='cart-item-update'),
    path('items/delete/<int:pk>/', CartItemDeleteView.as_view(), name='cart-item-delete'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]