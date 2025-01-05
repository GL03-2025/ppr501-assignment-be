from django.urls import path
from .views import HelloAPIView

urlpatterns = [
    path('', HelloAPIView.as_view(), name='hello'),
]