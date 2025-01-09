from django.urls import path
from categories.views import Categories, CategoryListView, CategoryCreateView, CategoryDetailView

urlpatterns = [
    # path('', Categories.as_view()),
    path('manage-categories/', CategoryListView.as_view({'get': 'list'}), name='manage-actegory'),
    path('manage-categorie/', CategoryCreateView.as_view(), name='category-create'),
    path('manage-categorie/<int:pk>/', CategoryDetailView.as_view(), name='user-detail'),
]
