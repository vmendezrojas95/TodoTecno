from django.shortcuts import render, redirect, get_object_or_404
from store.models import Productos, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Productos.objects.get(id=product_id)

    current_user = request.user

    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                
                try:
                    variation = Variation.objects.get(
                            producto=product,
                            variation_category__iexact=key,
                            variation_value__iexact=value,
                        )
                    product_variation.append(variation)
                except:
                    pass

        #return render(request, 'store/cart.html')


        is_cart_item_exists = CartItem.objects.filter(producto=product, user=current_user).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(producto=product, user=current_user)
            #existing variations -> database
            #current variations -> product_variation
            #item_id -> database
            #current item_id -> item_id
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # Incremetar la cantidad
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(producto=product, id=item_id)
                item.cantidad += 1
                item.save()
            else:
                # Crear un nuevo item
                item = CartItem.objects.create(
                        producto = product,
                        cantidad = 1,
                        user=current_user,
                    )
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)  
            item.save()
        else:
            cart_item = CartItem.objects.create(
                    producto = product,
                    cantidad = 1,
                    user = current_user,
                )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')



    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                
                try:
                    variation = Variation.objects.get(
                            producto=product,
                            variation_category__iexact=key,
                            variation_value__iexact=value,
                        )
                    product_variation.append(variation)
                except:
                    pass



        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                    cart_id = _cart_id(request)
                )
            cart.save()
        #return render(request, 'store/cart.html')


        is_cart_item_exists = CartItem.objects.filter(producto=product, cart=cart).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(producto=product, cart=cart)
            #existing variations -> database
            #current variations -> product_variation
            #item_id -> database
            #current item_id -> item_id
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # Incremetar la cantidad
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(producto=product, id=item_id)
                item.cantidad += 1
                item.save()
            else:
                # Crear un nuevo item
                item = CartItem.objects.create(
                        producto = product,
                        cantidad = 1,
                        cart = cart,
                    )
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)  
            item.save()
        else:
            cart_item = CartItem.objects.create(
                    producto = product,
                    cantidad = 1,
                    cart = cart,
                )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    
    product = get_object_or_404(Productos, id=product_id)
    
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(producto=product, user=request.user, id=cart_item_id)

        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(producto=product, cart=cart, id=cart_item_id)
        if cart_item.cantidad > 1:
            cart_item.cantidad -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass

    
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Productos, id=product_id)

    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(producto=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(producto=product, cart=cart, id=cart_item_id)
        
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, cantidad=0, cart_items=None):
    impuestos = 0
    total_general = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        
        for cart_item in cart_items:
            total += (cart_item.producto.producto_precio * cart_item.cantidad)
            cantidad += cart_item.cantidad
        impuestos = (21 * total)/100
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

@login_required(login_url='login')
def checkout(request, total=0, cantidad=0, cart_items=None):
    impuestos = 0
    total_general = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        
        for cart_item in cart_items:
            total += (cart_item.producto.producto_precio * cart_item.cantidad)
            cantidad += cart_item.cantidad
        impuestos = (21 * total)/100
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

    return render(request, 'store/checkout.html', context)