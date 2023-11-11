from django.db import models
from store.models import Productos, Variation


# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'Cart'
        ordering = ['date_added']
        verbose_name = 'Carrito'
        #verbose_name_plural = 'Carritos'

    def __str__(self):
        return self.cart_id
    

class CartItem(models.Model):
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'CartItem'
        verbose_name = 'Carrito Item'
        verbose_name_plural = 'Carrito Items'

    def sub_total(self):
        return self.producto.producto_precio * self.cantidad

    def __unicode__(self):
        return self.producto