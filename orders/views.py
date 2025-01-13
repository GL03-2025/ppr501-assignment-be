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
    if inputData:
        vnp = vnpay()
        vnp.responseData = inputData.dict()
        order_uuid = inputData['vnp_TxnRef']
        amount = int(inputData['vnp_Amount']) / 100
        order_desc = inputData['vnp_OrderInfo']
        transaction = inputData['vnp_TransactionNo']
        response= inputData['vnp_ResponseCode']
        # vnp_TmnCode = inputData['vnp_TmnCode']
        # vnp_PayDate = inputData['vnp_PayDate']
        # vnp_BankCode = inputData['vnp_BankCode']
        # vnp_CardType = inputData['vnp_CardType']

        if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
            if response == "00":  # Thanh toán thành công
                order = get_object_or_404(Order, order_uuid=order_uuid)
                order.status = OrderStatus.PAID.value
                order.save()
                if order.redirect_url:
                    return HttpResponseRedirect(order.redirect_url)
                return JsonResponse({
                    "title": "Kết quả thanh toán",
                    "result": "Thanh toán thành công",
                    "order_uuid": order_uuid,
                    "amount": amount,
                    "order_desc": order_desc,
                    "vnp_TransactionNo": transaction,
                    "vnp_ResponseCode": response
                })

            else:
                return JsonResponse({
                    "title": "Kết quả thanh toán",
                    "result": "Lỗi",
                    "order_uuid": order_uuid,
                    "amount": amount,
                    "order_desc": order_desc,
                    "vnp_TransactionNo": transaction,
                    "vnp_ResponseCode": response
                })
        else:
            # Sai checksum
            return JsonResponse({
                "title": "Kết quả thanh toán",
                "result": "Lỗi",
                "order_uuid": order_uuid,
                "amount": amount,
                "order_desc": order_desc,
                "vnp_TransactionNo": transaction,
                "vnp_ResponseCode": response,
                "msg": "Sai checksum"
            })
    else:
        return JsonResponse({
            "title": "Kết quả thanh toán",
            "result": "Không có dữ liệu"
        })
