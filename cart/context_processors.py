from .models import Cart , CartItem
from cart.views import _cart_id


# def counter(request,quantity=0,total=0):
#     grand_total=0
#     tax=0
#     if 'admin' in request.path:
#         return{}
#     else:
#         try:
#             cart=Cart.objects.get(cart_id=_cart_id(request))
#             if request.user.is_authenticated:
#                  cart_items=CartItem.objects.all().filter(user=request.user)
#             else:
#                 cart_items=CartItem.objects.all().filter(cart=cart[:1])
#             for cart_item in cart_items:
#                 total +=(cart_item.product.price * cart_item.quantity)
#                 quantity +=cart_item.quantity
#             tax=(2 * total)/100
#             grand_total =total +tax
#         except Cart.DoesNotExist:
#             cart_item=0


#     context={
#         'quantity':quantity,
#         'grand_total':grand_total
#     }
#     return dict(context)

def counter(request):
    cart_count=0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart=Cart.objects.filter(cart_id=_cart_id(request))
            if request.user.is_authenticated:
                cart_items=CartItem.objects.all().filter(user=request.user)
            else:
                cart_items=CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except:
            cart_count=0
    context={
        'quantity':cart_count,
           
    }
    return dict(context)
