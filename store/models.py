from django.db import models
from categoria.models import Categoria
from django.urls import reverse

# Create your models here.

class Productos(models.Model):
    producto_nombre = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    producto_descripcion = models.TextField(max_length=500, blank=True)
    producto_precio = models.DecimalField(max_digits=10, decimal_places=2)
    producto_imagen = models.ImageField(upload_to='fotos/productos', blank=True)
    producto_stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

        
        
    def get_url(self):
        return reverse('product_detail', args=[self.categoria.slug, self.slug])

    
    
    
    def __str__(self):
        return self.producto_nombre
    

