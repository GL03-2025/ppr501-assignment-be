from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from accounts import views
from accounts.views import RequestPasswordResetEmail, UserListView, UserDetailView

router = DefaultRouter()
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='auth_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('new-password/', views.SetNewPasswordView.as_view(), name='change_password'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),name="request-reset-email"),
    path('manage-accounts/', UserListView.as_view({'get': 'list'}), name='manage-account'),
    path('manage-account/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    # Test ==================================
    # path('test/', views.testEndPoint, name='test'),
    # path("test_post", views.MyView.as_view(), name="test_post"),
    # ========================================
]