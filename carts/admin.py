from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_id', 'date_added']
    list_filter = ['date_added']
    search_fields = ['cart_id']

class CartItemAdmin(admin.ModelAdmin):
    list_display = ['producto', 'cart', 'cantidad', 'is_active']
    list_filter = ['producto']
    search_fields = ['producto']

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
