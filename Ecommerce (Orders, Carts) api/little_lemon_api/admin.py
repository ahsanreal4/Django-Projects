from django.contrib import admin
from .models import Cart,Category,MenuItem,Order,OrderItem

# Register your models here.
admin.site.register([Cart, Category, MenuItem, Order, OrderItem])
