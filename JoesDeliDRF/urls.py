from django.urls import path, include
from rest_framework.routers import DefaultRouter
from JoesDeliDRF.views import CustomTokenCreateView

from .views import (
    MenuItemViewSet,
    OrderViewSet,
    OrderItemViewSet,
    RatingViewSet,
    TestTokenView
)

router = DefaultRouter()
router.register(r'menu-items', MenuItemViewSet, basename='menu-items')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'order-items', OrderItemViewSet, basename='orderitem')
router.register(r'ratings', RatingViewSet, basename='rating')

urlpatterns = [
    path('', include(router.urls)),
    path('test-token/', TestTokenView.as_view()),  # ✅ now properly registered
    path('auth/jwt/create/', CustomTokenCreateView.as_view(), name='custom_token_create'),
]
