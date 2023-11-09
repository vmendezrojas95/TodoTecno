from django.shortcuts import render
from store.models import Productos

# Create your views here.
def home(request):
    products = Productos.objects.all().filter(is_available=True).order_by('created_date')
    context = {
        'products': products,
    }
    return render(request, 'home.html', context)