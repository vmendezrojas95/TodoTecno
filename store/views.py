from django.shortcuts import render, get_object_or_404
from .models import Productos
from categoria.models import Categoria
from carts.models import CartItem, Cart
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

# Create your views here.
def store(request, category_slug=None):
    categorias = None
    products = None

    if category_slug != None:
        categorias = get_object_or_404(Categoria, slug=category_slug)
        products = Productos.objects.filter(categoria=categorias, is_available=True).order_by('id')
        paginator = Paginator(products, 5)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()
    else:
        products = Productos.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 5)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()


    context = {
        'products': paged_products,
        'products_count': products_count,
    }

    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Productos.objects.get(categoria__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), producto=single_product).exists()
    except Exception as e:
        raise e
    
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
   
    return render(request, 'store/product_detail.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Productos.objects.order_by('-created_date').filter(Q(producto_descripcion__icontains=keyword) | Q(producto_nombre__icontains=keyword))
            products_count = products.count()
    context = {
        'products': products,
        'products_count': products_count,
    }
    return render(request, 'store/store.html', context)