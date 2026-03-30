from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title


# models.py
class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)     
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)

    
    def __str__(self):
        return self.title

class Rating(models.Model):
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    rating = models.SmallIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.menuitem.title} x {self.quantity}"

class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='customer_orders'  # 🔹 Distinct reverse accessor
    )
    delivery_crew = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_deliveries'  # 🔹 Distinct reverse accessor
    )
    status = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
     # 🔹 New fields
    estimated_delivery = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    priority = models.CharField(
        max_length=10,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        default='medium'
    )
    def __str__(self):
        return f"{self.menuitem.title} x {self.quantity} for Order #{self.order.id}"
    

