from django.shortcuts import get_object_or_404, render
from .models import Category
from store.models import Product
# Create your views here.

def store(request,category_slug=None):
    #to show category wise product
    all_category=Category.objects.all().order_by('category_name')
    categories=None
    all_product=None

    if category_slug !=None:
        categories=get_object_or_404(Category,slug=category_slug)
        all_product=Product.objects.filter(category=categories,is_available=True)
        product_count=all_product.count()
    else:
        all_product=Product.objects.all().order_by('-created_date')
        product_count=all_product.count()
        
    return render(request,'store/store.html',{
        'all_product':all_product,
        'product_count':product_count,
        'all_category':all_category,

    })


    #product detail


def product_detail(request,category_slug,product_slug):

    try:
        single_product=Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    return render(request,'store/product_detail.html' ,{
        'single_product':single_product
    })
