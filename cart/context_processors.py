from .models import Cart , CartItem
from cart.views import _cart_id


def counter(request,quantity=0,total=0):
    if 'admin' in request.path:
        return{}
    else:
        try:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,is_active=True)
            for cart_item in cart_items:
                total +=(cart_item.product.price * cart_item.quantity)
                quantity +=cart_item.quantity
            tax=(2 * total)/100
            grand_total =total +tax
        except Cart.DoesNotExist:
            cart_item=0


    context={
        'quantity':quantity,
        'grand_total':grand_total
    }
    return dict(context)