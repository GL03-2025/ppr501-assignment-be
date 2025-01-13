from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from orders.models import Order, OrderDetail
from accounts.models import AccountDetail

class CartView(generics.RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

class CartItemView(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)

class CartItemUpdateView(generics.UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

class CartItemDeleteView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

class CheckoutView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items.exists():
            return Response({'message': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        account_detail, created = AccountDetail.objects.get_or_create(user=user)
        order = Order.objects.create(
            accountId=account_detail,
            amount=sum(item.product.price * item.quantity for item in cart_items),
            status='active',
            description='Order created from cart',
            content='',
            notes='',
            method='payment method'
        )

        for item in cart_items:
            OrderDetail.objects.create(
                orderId=order,
                productId=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        cart_items.delete()

        return Response({'message': 'Order created successfully', 'order_id': order.id}, status=status.HTTP_201_CREATED)