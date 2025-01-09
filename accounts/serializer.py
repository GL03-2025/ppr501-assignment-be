from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from accounts.models import User, UserStatus
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from django_filters.rest_framework import FilterSet, filters

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # These are claims, you can add custom claims
        token['id'] = user.id
        token['username'] = user.username
        token['email'] = user.email
        token['phone'] = user.phone
        token['address'] = user.address
        token['status'] = user.status
        # ...
        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])

    # Để giá trị mặc định là 'active' nếu người dùng không cung cấp
    status = serializers.ChoiceField(
        choices=[(status.value, status.name) for status in UserStatus],
        required=False,
        default='active'  # Giá trị mặc định là 'active'
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'last_name', 'first_name', 'password', 'phone', 'address', 'image', 'status')

    def create(self, validated_data):
        # Lấy giá trị status từ validated_data, nếu không có thì mặc định là 'active'
        status = validated_data.get('status', 'active')

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            address=validated_data['address'],
            image=validated_data['image'],
            status=status,
            last_name=validated_data['last_name'],
            first_name=validated_data['first_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    class Meta:
        fields = ['password', 'token', 'uidb64']
    def validate(self, attrs):
        uidb64 = attrs['uidb64']
        token = attrs['token']
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('Invalid or expired token.', 401)
            attrs['user'] = user
        except (User.DoesNotExist, ValueError, TypeError):
            raise AuthenticationFailed('Invalid user or token.', 404)
        return attrs

    def save(self):
        user = self.validated_data['user']
        user.set_password(self.validated_data['password'])
        user.save()

class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    class Meta:
        fields = ['email']

# map dữ liệu từ model sang json
class GetAccountSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=UserStatus.choices())
    class Meta:
        model = User
        fields = '__all__'
       # depth = 1 Dùng để lấy các bảng con

class UpdateAccountSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=UserStatus.choices())
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'address', 'image', 'status']
# Phân trang
class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        current_page = self.page.number
        total_pages = self.page.paginator.num_pages
        total_count = self.page.paginator.count
        page_size = self.get_page_size(self.request)
        return Response({
            'count': total_count,
            'page_size': page_size,
            'total_pages': total_pages,
            'current_page': current_page,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
# Lọc dữ liệu
class UserFilter(FilterSet):
    status = filters.CharFilter(field_name='status', lookup_expr='exact') # Tra cứu chính xác
    name = filters.CharFilter(field_name='username', lookup_expr='icontains') # Tra cứu chuỗi con, không phân biệt chữ hoa/thường
    # class Meta:
    #     model = User
    #     fields = ['status','username']


# ======================= Test =======================
class MySerializer(serializers.Serializer):
    token = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()