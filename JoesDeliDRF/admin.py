from django.contrib import admin
from .models import MenuItem, Cart, Order, OrderItem, Rating, Category
from .models import Category

admin.site.register(MenuItem)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Rating)
admin.site.register(Category)
