from django.urls import path

from . import views
from .views import  OrderDetailView,  OrderDeleteView, OrderTmpCreateView, OrderTmpListView

urlpatterns = [
   # path('', OrderListView.as_view(), name='order-list'),
   # path('create/', OrderCreateView.as_view(), name='order-create'),
   # path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
   # path('<int:pk>/delete/', OrderDeleteView.as_view(), name='order-delete'),

    path('manage-order/<int:pk>/',  OrderDetailView.as_view(), name='order-detail'),
    path('manage-orders/', OrderTmpListView.as_view({'get': 'list'}), name='manage-order'),
    path('manage-order/', OrderTmpCreateView.as_view(), name='order-create-tmp'),
    path('payment/return/', views.payment_return, name='payment_return'),
]