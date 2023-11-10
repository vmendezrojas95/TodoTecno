from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('store.html', views.store, name='store_html'),
    path('categoria<slug:category_slug>/', views.store, name='products_by_category'),
    path('cateogira<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
]