from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.generics import GenericAPIView
from accounts.models import User
from accounts.serializer import MyTokenObtainPairSerializer, RegisterSerializer, MySerializer, SetNewPasswordSerializer, \
    ResetPasswordEmailRequestSerializer, GetAccountSerializer, CustomPagination, UserFilter, UpdateAccountSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from django_filters.rest_framework import DjangoFilterBackend

from accounts.utils import Util


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    # queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'User added successfully'}, status=status.HTTP_201_CREATED)

class SetNewPasswordView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SetNewPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            email_body = f"Hello,<br><br>Use the following token to reset your password:<br><br>Token: {token}<br>UID: {uidb64}"
            data = {
                'email_body': email_body,
                'to_email': user.email,
                'email_subject': 'Reset Your Password',
            }
            Util.send_email(data)

        return Response({'success': 'We have sent you a token to reset your password'}, status=status.HTTP_200_OK)

class UserListView(viewsets.ModelViewSet):
    queryset = User.objects.all() # Lấy tất cả dữ liệu từ model
    serializer_class = GetAccountSerializer # Gọi map model sang json
    pagination_class = CustomPagination # Phân trang
    filter_backends = [DjangoFilterBackend] # Lọc dữ liệu
    filterset_class = UserFilter # Lọc dữ liệu
    # permission_classes = [IsAuthenticated]  # Phân quyền

# Cái này nó sẽ tự làm ra 4 hàm GET, POST, PUT, DELETE cho mình cần phải handler lại nó ( Có thể không handler)
# class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UpdateAccountSerializer
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateAccountSerializer

    # def get(self, request, *args, **kwargs):
    #     user = self.get_object()
    #     serializer = self.get_serializer(user)
    #     return Response(serializer.data)
    #
    # def put(self, request, *args, **kwargs):
    #     user = self.get_object()
    #     serializer = self.get_serializer(user, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def patch(self, request, *args, **kwargs):
    #     user = self.get_object()
    #     serializer = self.get_serializer(user, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def delete(self, request, *args, **kwargs):
    #     user = self.get_object()
    #     user.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


#================================= Test API=================================
# Không sài

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulation {request.user}, your API just responded to GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = "Hello buddy"
        data = f'Congratulation your API just responded to POST request with text: {text}'
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST)

# API Post Have Body
class MyView(GenericAPIView):
    serializer_class = MySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        return Response(data, status=status.HTTP_200_OK)

#================================= Test API=================================