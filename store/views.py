from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Category
from store.models import Product,Variation
from cart.views import _cart_id
from cart.models import Cart,CartItem
#paginator
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
# Create your views here.

#show store
def store(request,category_slug=None):
    #to show category wise product
    all_category=Category.objects.all().order_by('category_name')
    categories=None
    all_product=None

    if category_slug !=None:
        categories=get_object_or_404(Category,slug=category_slug)
        all_product=Product.objects.filter(category=categories,is_available=True)
          #paginator
        paginator=Paginator(all_product,1)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
        product_count=all_product.count()
    else:
        all_product=Product.objects.all().order_by('-created_date')
        #for paginator
        paginator=Paginator(all_product,6)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)#only 6 products stored in pages product
        product_count=all_product.count()
        
    return render(request,'store/store.html',{
        'all_product':paged_products,#that 6 product pass into paged product
        'product_count':product_count,
        'all_category':all_category,
        

    })


    #product detail


def product_detail(request,category_slug,product_slug):


    try:
        single_product=Product.objects.get(category__slug=category_slug, slug=product_slug)
        #if this product is inside the cart
        in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    except Exception as e:
        raise e
    return render(request,'store/product_detail.html' ,{
        'single_product':single_product,
        'in_cart':in_cart,
      
        
    })

#search

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            all_product=Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count=all_product.count()
        else:
            return redirect('store:store')

    return render(request,'store/store.html',{
        'all_product':all_product,
        'product_count':product_count
    })

