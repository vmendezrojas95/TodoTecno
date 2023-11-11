from django.contrib import admin
from .models import Productos, Variation

# Register your models here.

class ProductosAdmin(admin.ModelAdmin):
    list_display = ('producto_nombre', 'producto_precio', 'producto_stock', 'categoria' , 'modified_date' , 'is_available')
    prepopulated_fields = {'slug': ('producto_nombre',)}
    readonly_fields = ('created_date', 'modified_date')

class VariationAdmin(admin.ModelAdmin):
    list_display = ('producto', 'variation_category', 'variation_name', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('producto', 'variation_category', 'variation_name', 'variation_value', 'is_active')
    #list_per_page = 50

admin.site.site_header = 'Administracion de Tienda'
admin.site.register(Productos, ProductosAdmin)
admin.site.register(Variation, VariationAdmin)

