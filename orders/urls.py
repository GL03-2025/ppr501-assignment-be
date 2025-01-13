from django.urls import path
from .views import OrderCreateView, OrderDetailView, OrderListView, OrderDeleteView, OrderTmpCreateView, \
    OrderTmpListView

urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:pk>/delete/', OrderDeleteView.as_view(), name='order-delete'),

    path('manage-orders/', OrderTmpListView.as_view({'get': 'list'}), name='manage-order'),
    path('manage-order/', OrderTmpCreateView.as_view(), name='order-create-tmp'),
]