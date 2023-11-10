from django.shortcuts import render, redirect, get_object_or_404
from store.models import Productos
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Productos.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()
    #return render(request, 'store/cart.html')

    try:
        cart_item = CartItem.objects.get(producto=product, cart=cart)
        cart_item.cantidad += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
                producto = product,
                cantidad = 1,
                cart = cart,
            )
        cart_item.save()
    return redirect('cart')


def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Productos, id=product_id)
    cart_item = CartItem.objects.get(producto=product, cart=cart)
    if cart_item.cantidad > 1:
        cart_item.cantidad -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Productos, id=product_id)
    cart_item = CartItem.objects.get(producto=product, cart=cart)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, cantidad=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        
        for cart_item in cart_items:
            total += (cart_item.producto.producto_precio * cart_item.cantidad)
            cantidad += cart_item.cantidad
        impuestos = (18 * total)/100
        total_general = total + impuestos
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total':total,
        'cantidad':cantidad,
        'cart_items':cart_items,
        'impuestos':impuestos,
        'total_general' : total_general,
    }

    return render(request, 'store/cart.html', context)