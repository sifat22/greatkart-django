from store.models import Product
from django.shortcuts import render
from store.models import Product


def index(request):
    prodcuct=Product.objects.all().filter(is_available=True)
    return render(request, 'index.html',{
        'product':prodcuct
    })