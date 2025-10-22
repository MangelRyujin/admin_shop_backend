from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.products.api.views.product_view import ProductViewSet 
from apps.products.api.views.offert_view import OffertViewSet
from apps.products.api.views.category_view import CategoryViewSet, SubCategoryViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products'),
router.register(r'offerts', OffertViewSet, basename='offerts'),
router.register(r'categories', CategoryViewSet, basename='categories'),
router.register(r'subcategories', SubCategoryViewSet, basename='subcategories'),

urlpatterns = [
    path('', include(router.urls)),
]