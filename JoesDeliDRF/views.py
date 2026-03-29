from datetime import datetime, time
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status, serializers, permissions, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from JoesDeliDRF.token_serializers import CustomTokenCreateSerializer
from .models import MenuItem, Cart, Order, OrderItem, Rating
from .serializers import (
    MenuItemSerializer,
    CartSerializer,
    OrderSerializer,
    OrderItemSerializer,
    RatingSerializer
)
from .permissions import IsManager, IsDeliveryCrew
from rest_framework.decorators import action


# 🔧 Utility for timezone-aware filtering
def get_today_utc_range():
    local_today = timezone.localtime().date()
    start_local = datetime.combine(local_today, time.min)
    end_local = datetime.combine(local_today, time.max)
    start_utc = timezone.make_aware(start_local).astimezone(timezone.utc)
    end_utc = timezone.make_aware(end_local).astimezone(timezone.utc)
    return start_utc, end_utc

# 🔹 Root view
def root_view(request):
    return JsonResponse({
        "message": "Welcome to the Joe's Deli API",
        "available_endpoints": [
            "/api/menu-items/",
            "/api/cart-items/",
            "/api/orders/",
            "/api/order-items/",
            "/api/ratings/"
        ]
    })

# 🔹 Group Management
class GroupManagementViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def list(self, request, group_name=None):
        try:
            group = Group.objects.get(name__iexact=group_name)
            users = group.user_set.all()
            user_data = [{'id': u.id, 'username': u.username, 'email': u.email} for u in users]
            return Response(user_data)
        except Group.DoesNotExist:
            return Response({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, group_name=None):
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            group = Group.objects.get(name__iexact=group_name)
            group.user_set.add(user)
            return Response({'message': f'User {user.username} added to {group_name}'}, status=status.HTTP_201_CREATED)
        except (User.DoesNotExist, Group.DoesNotExist):
            return Response({'error': 'User or group not found'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, group_name=None, user_id=None):
        try:
            user = User.objects.get(id=user_id)
            group = Group.objects.get(name__iexact=group_name)
            group.user_set.remove(user)
            return Response({'message': f'User {user.username} removed from {group_name}'})
        except (User.DoesNotExist, Group.DoesNotExist):
            return Response({'error': 'User or group not found'}, status=status.HTTP_404_NOT_FOUND)

# 🔹 Menu Items
class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'category__title']
    ordering_fields = ['price', 'title']
    ordering = ['title']
    filterset_fields = ['category', 'price']

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsManager()]
        return []

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset.exists():
            return Response({"message": "No items found in this category"})
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# 🔹 Cart
class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        menuitem = serializer.validated_data['menuitem']
        quantity = serializer.validated_data['quantity']
        unit_price = menuitem.price
        price = unit_price * quantity
        serializer.save(user=self.request.user, unit_price=unit_price, price=price)

    def create(self, request, *args, **kwargs):
        menuitem = request.data.get('menuitem')
        quantity = int(request.data.get('quantity', 1))

        existing = Cart.objects.filter(user=request.user, menuitem_id=menuitem).first()
        if existing:
            existing.quantity += quantity
            existing.price = existing.unit_price * existing.quantity
            existing.save()
            return Response(CartSerializer(existing).data)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        Cart.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['delete'], url_path='clear')
    def clear_cart(self, request):
        Cart.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 🔹 Orders
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        date_filter = self.request.query_params.get('date')

        if date_filter == 'today':
            start_utc, end_utc = get_today_utc_range()
            base_qs = Order.objects.filter(date__range=(start_utc, end_utc))
        else:
            base_qs = Order.objects.all()

        if user.groups.filter(name='Manager').exists():
            return base_qs
        elif user.groups.filter(name='Delivery crew').exists():
            return base_qs.filter(delivery_crew=user)
        return base_qs.filter(user=user)

    def perform_create(self, serializer):
        user = self.request.user
        cart_items = Cart.objects.filter(user=user)
        if not cart_items.exists():
            raise serializers.ValidationError("Cart is empty.")
        order = serializer.save(user=user)
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                menuitem=item.menuitem,
                quantity=item.quantity,
                unit_price=item.unit_price,
                price=item.price
            )
        cart_items.delete()

    def update(self, request, *args, **kwargs):
        user = request.user
        order = self.get_object()
        if user.groups.filter(name='Manager').exists():
            return super().update(request, *args, **kwargs)
        elif user.groups.filter(name='Delivery crew').exists():
            status_value = request.data.get('status')
            if status_value in ['0', '1']:
                order.status = int(status_value)
                order.save()
                return Response({'status': 'updated'})
            return Response({'error': 'Invalid status or unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if user.groups.filter(name='Manager').exists():
            return super().destroy(request, *args, **kwargs)
        return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

# 🔹 Order Items
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

# 🔹 Ratings
class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

class TestTokenView(APIView):
    permission_classes = [AllowAny]  # ✅ allow unauthenticated access

    def post(self, request):
        from .token_serializers import CustomTokenCreateSerializer
        serializer = CustomTokenCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
    def get(self, request):
        return Response({"message": "GET method works"})

class CustomTokenCreateView(TokenObtainPairView):
    serializer_class = CustomTokenCreateSerializer

