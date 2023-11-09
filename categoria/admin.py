from django.contrib import admin
from .models import Categoria

# Register your models here.

class CategoriaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('categoria_nombre',)}
    list_display = ('categoria_nombre', 'slug')
    #readonly_fields = ('created', 'updated')

admin.site.register(Categoria, CategoriaAdmin)