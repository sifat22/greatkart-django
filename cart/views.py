from django.contrib.sites import requests
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.expressions import Value
from cart.models import Cart
from django.shortcuts import get_object_or_404, redirect, render
from store.models import Product,Variation
from cart.models import Cart,CartItem
from django.contrib.auth.decorators import login_required

# Create your views here.
#only adding productt in cart
#getting session id
def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request,product_id):
    current_user=request.user
    product=Product.objects.get(id=product_id)#get the product #add cart
    # if user is authenticated
    if current_user.is_authenticated:
        product_variation=[]
        if request.method=='POST':
            for item in request.POST:
                key=item
                value=request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key,variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
                     
        #adding cart Item
        is_cart_item_exists=CartItem.objects.filter(product=product,user=current_user).exists()
        if is_cart_item_exists:
            cart_item=CartItem.objects.filter(product=product,user=current_user)
            #existing variation
            #current variation
            #item_id
            ex_var_list=[]
            id=[]
            for item in cart_item:
                existing_variation=item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
           

            if product_variation in ex_var_list:
                #increase cart quantity
                index=ex_var_list.index(product_variation)
                item_id=id[index]
                item=CartItem.objects.get(product=product,id=item_id)
                item.quantity +=1
                item.save()
                    
            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                #add variation
                if len(product_variation) >0: #add variation
                    item.variations.clear() #add variation
                    #add variation
                    item.variations.add(*product_variation) #add variation
                
                #cart_item.quantity +=1#add cart
                item.save()#add cart
            
        else:  
            cart_item=CartItem.objects.create(     #add cart
                product=product,#add cart
                quantity=1,#add cart
                user=current_user,

            )
            #add variation
            if len(product_variation) >0: #add variation
                cart_item.variations.clear() #add variation
            
                cart_item.variations.add(*product_variation) #add variation
            cart_item.save()#add cart
        return redirect('app_cart:cart')#add cart

       
#if the user is not authenticated
    else:
        product_variation=[]
        if request.method=='POST':
            for item in request.POST:
                key=item
                value=request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key,variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
        
        #add cart
        try:
            cart=Cart.objects.get(cart_id=_cart_id(request))#get the cart using the cart id with seesion
        except Cart.DoesNotExist:
            cart=Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()
        #adding cart Item
        is_cart_item_exists=CartItem.objects.filter(product=product,cart=cart).exists()
        if is_cart_item_exists:
            cart_item=CartItem.objects.filter(product=product,cart=cart)
            #existing variation
            #current variation
            #item_id
            ex_var_list=[]
            id=[]
            for item in cart_item:
                existing_variation=item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            print(ex_var_list)

            if product_variation in ex_var_list:
                #increase cart quantity
                index=ex_var_list.index(product_variation)
                item_id=id[index]
                item=CartItem.objects.get(product=product,id=item_id)
                item.quantity +=1
                item.save()
                    
            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                #add variation
                if len(product_variation) >0: #add variation
                    item.variations.clear() #add variation
                    #add variation
                    item.variations.add(*product_variation) #add variation
                
                #cart_item.quantity +=1#add cart
                item.save()#add cart
            
        else:  
            cart_item=CartItem.objects.create(     #add cart
                product=product,#add cart
                quantity=1,#add cart
                cart=cart,#add cart

            )
            #add variation
            if len(product_variation) >0: #add variation
                cart_item.variations.clear() #add variation
            
                cart_item.variations.add(*product_variation) #add variation
            cart_item.save()#add cart
        return redirect('app_cart:cart')#add cart

#decrease  cart
def remove_cart(request,product_id,cart_item_id):#cart_item_id added after variation
    product=get_object_or_404(Product,id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item=CartItem.objects.get(product=product,user=request.user,id=cart_item_id)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_item=CartItem.objects.get(product=product,cart=cart,id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('app_cart:cart')

       

 # remove cart for 
def remove_cart_item(request,product_id,cart_item_id):
    product=get_object_or_404(Product,id=product_id)
    if request.user.is_authenticated:
        cart_item=CartItem.objects.get(product=product,user=request.user,id=cart_item_id)
    else:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_item=CartItem.objects.get(product=product,cart=cart,id=cart_item_id)
    cart_item.delete()
    return redirect('app_cart:cart')


#remove cart whishlist when we make it

# def remove_cart_item(request,product_id):
#     cart=Cart.objects.get(cart_id=_cart_id(request))
#     product=get_object_or_404(Product,id=product_id)
#     cart_item=CartItem.objects.get(product=product,cart=cart)
#     cart_item.delete()
#     return redirect('app_cart:cart')




#showing product name totl and quntity in cart
def cart(request,total=0,quantity=0,cart_items=None):
    try:
        grand_total=0
        tax=0
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total +=(cart_item.product.price * cart_item.quantity)
            quantity +=cart_item.quantity
        tax=(2 * total)/100
        grand_total =total +tax
    except ObjectDoesNotExist:
        pass


    return render(request,'store/cart.html',{
       'total':total,
       'quantity':quantity,
       'cart_items':cart_items,
       'tax':tax,
       'grand_total':grand_total,

    })



# def cart(request,total=0,quantity=0,cart_items=None):
#     try:
#         grand_total=0
#         tax=0
#         cart=Cart.objects.get(cart_id=_cart_id(request))
#         if request.user.is_authenticated:
#             cart_items=CartItem.objects.filter(user=request.user,is_active=True)
#         else:
#             cart_items=CartItem.objects.filter(cart=cart,is_active=True)
#         for cart_item in cart_items:
#             total +=(cart_item.product.price * cart_item.quantity)
#             quantity +=cart_item.quantity
#         tax=(2 * total)/100
#         grand_total =total +tax
#     except ObjectDoesNotExist:
#         pass


#     return render(request,'store/cart.html',{
#        'total':total,
#        'quantity':quantity,
#        'cart_items':cart_items,
#        'tax':tax,
#        'grand_total':grand_total,

#     })
            



#checkout
@login_required(login_url='app_login:login')
def checkout(request,total=0,quantity=0,cart_items=None):
    try:
        grand_total=0
        tax=0
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total +=(cart_item.product.price * cart_item.quantity)
            quantity +=cart_item.quantity
        tax=(2 * total)/100
        grand_total =total +tax
    except ObjectDoesNotExist:
        pass


    return render(request,'store/checkout.html',{
       'total':total,
       'quantity':quantity,
       'cart_items':cart_items,
       'tax':tax,
       'grand_total':grand_total,

    })
