from xmlrpc.client import Fault

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from accounts.models import AccountDetail
from django.conf import settings
from accounts.serializer import CustomPagination
from .models import Order, OrderStatus
from .serializer import OrderSerializer, CreateOrderResponseSerializer, OrderCreateSerializer, GetAllOrderSerializer, \
    OrderFilter
from rest_framework.exceptions import NotFound

from .vnpay import vnpay

class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            order = serializer.instance
            response_data = CreateOrderResponseSerializer(order).data
            response_data['message'] = 'Order created successfully'
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'message': 'Order creation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        account_detail, created = AccountDetail.objects.get_or_create(user=self.request.user)
        serializer.save(accountId=account_detail)

class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = CreateOrderResponseSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        order = super().get_object()
        if order.accountId.user != self.request.user:
            raise NotFound("You do not have permission to view this order.")
        return order

class OrderListView(generics.ListAPIView):
    serializer_class = CreateOrderResponseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(accountId__user=self.request.user)

    def get_object(self):
        try:
            order = Order.objects.get(pk=self.kwargs['pk'], accountId__user=self.request.user)
        except Order.DoesNotExist:
            raise NotFound("Order not found.")
        return order


class OrderDeleteView(generics.DestroyAPIView):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            order = Order.objects.get(pk=self.kwargs['pk'], accountId__user=self.request.user)
        except Order.DoesNotExist:
            raise NotFound("Order not found.")
        if order.accountId.user != self.request.user:
            raise NotFound("You do not have permission to delete this order.")
        return order

    def destroy(self, request, *args, **kwargs):
        order = self.get_object()
        order.status = 'inactive'
        order.save()
        return Response({
            'message': 'Order status changed to inactive successfully'
        }, status=status.HTTP_200_OK)

class OrderTmpListView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = GetAllOrderSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter
    # permission_classes = [IsAuthenticated]  # Phân quyền

class OrderTmpCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    #permission_classes = [IsAuthenticated]

# Không cần bật phân quyền cho API này
@api_view(['GET'])
def payment_return(request):
    inputData = request.GET
    if inputData and 'vnp_TxnRef' in inputData and 'vnp_ResponseCode' in inputData:
        vnp = vnpay()
        vnp.responseData = inputData.dict()
        order_uuid = inputData['vnp_TxnRef']
        amount = int(inputData['vnp_Amount']) / 100
        order_desc = inputData.get('vnp_OrderInfo', '')
        transaction = inputData.get('vnp_TransactionNo', '')
        response = inputData['vnp_ResponseCode']
        if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
            try:
                order = get_object_or_404(Order, order_uuid=order_uuid)
                if response == "00":
                    order.status = OrderStatus.PAID.value
                    order.save()
                    success = True
                else:
                    success = False
                if order.redirect_url:
                    return_url = f"{order.redirect_url}?order_id={order.id}&success={str(success).lower()}"
                    return HttpResponseRedirect(return_url)
            except Exception as e:
                print(f"Error processing payment: {e}")
    return HttpResponseRedirect('/error')
