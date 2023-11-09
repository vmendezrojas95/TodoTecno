from django.shortcuts import render, get_object_or_404
from .models import Productos
from categoria.models import Categoria

# Create your views here.
def store(request, category_slug=None):
    categorias = None
    products = None

    if category_slug != None:
        categorias = get_object_or_404(Categoria, slug=category_slug)
        products = Productos.objects.filter(categoria=categorias, is_available=True)
        products_count = products.count()
    else:
        products = Productos.objects.all().filter(is_available=True)
        products_count = products.count()


    context = {
        'products': products,
        'products_count': products_count,
    }

    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Productos.objects.get(categoria__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    
    context = {
        'single_product': single_product,
    }
   
    return render(request, 'store/product_detail.html', context)