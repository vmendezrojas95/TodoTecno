from django.db import models

# Create your models here.
class Categoria(models.Model):
    categoria_nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(max_length=50, unique=True)
    categoria_imagen = models.ImageField(upload_to='fotos/categoria', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['categoria_nombre']

    def __str__(self):
        return self.categoria_nombre