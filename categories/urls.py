from django.urls import path
from categories.views import Categories

urlpatterns = [
    path('', Categories.as_view()),
]
