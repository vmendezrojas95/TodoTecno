from django.contrib import admin
from .models import Productos

# Register your models here.

class ProductosAdmin(admin.ModelAdmin):
    list_display = ('producto_nombre', 'producto_precio', 'producto_stock', 'categoria' , 'modified_date' , 'is_available')
    prepopulated_fields = {'slug': ('producto_nombre',)}
    readonly_fields = ('created_date', 'modified_date')

admin.site.register(Productos, ProductosAdmin)