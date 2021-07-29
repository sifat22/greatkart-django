from django.contrib import messages,auth
from django.contrib.auth import tokens
from django.http.response import HttpResponse
from accounts.models import Account
from django.shortcuts import redirect, render
from.forms import RegistrationForm
from django.contrib.auth.decorators import login_required

#User Activation  Varification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from cart.views import _cart_id
from cart.models import Cart,CartItem
from store.models import Product,Variation


# after installing requests
import requests




# Create your views here.

#login
def login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']

        user=auth.authenticate(email=email,password=password)

        if user is not None:
            try:
                cart=Cart.objects.get(cart_id=_cart_id(request))# if there is any cart item insite this user
                is_cart_item_exists=CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item=CartItem.objects.filter(cart=cart)

                    #getting the product variation by cart id
                    product_variation=[]
                    for item in cart_item:
                        variation=item.variations.all()
                        product_variation.append(list(variation))

                    #get the cart items from the user to ccess his prouct variations
                    cart_item=CartItem.objects.filter(user=user)
                    #existing variation
                    #current variation
                    #item_id
                    ex_var_list=[]
                    id=[]
                    for item in cart_item:
                        existing_variation=item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    #get the common variation so that it increases quantity not product in the cart
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index=ex_var_list.index(pr)
                            item_id =id[index]
                            item=CartItem.objects.get(id=item_id)
                            item.quantity +=1
                            item.user=user
                            item.save()
                        else:
                            cart_item=CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()                   
            except:
                pass
            auth.login(request,user)
            messages.success(request,"You are logged in")
            #after import request
            url=request.META.get('HTTP_REFERER')
            try:
                query=requests.utils.urlparse(url).query
                params=dict(x.split('=')for x in query.split('&'))
                if 'next' in params:
                    nextPage=params['next']
                    return redirect(nextPage)
            except:
                #before importing request
                return redirect('app_login:dashboard')
            
        else:
            messages.error(request,"invalid login conditional")
            return redirect('app_login:login')
    return render (request,'accounts/login.html')



#register
def register(request):
    #create user
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data.get('first_name')
            last_name=form.cleaned_data.get('last_name')
            phone_number=form.cleaned_data.get('phone_number')
            email=form.cleaned_data.get('email')
            password=form.cleaned_data.get('password')
            username=email.split("@")[0]

            user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number=phone_number
            user.save()

            #User Activation  er jnne default reg er kichui change kora hoinai
            current_site = get_current_site(request)
            mail_subject = 'Please Activate your account!'
            message = render_to_string('accounts/account_verify_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_mail = EmailMessage(mail_subject, message, to=[to_email])
            send_mail.send()

            #success registration message  before activing user we can use this
            #messages.success(request,'Thank You for registering with us.We have sent you verification email to youor email address')
            #after user activation the success message are
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form=RegistrationForm()
    return render (request,'accounts/register.html',{
        'form':form,
    })

#user varification email 
def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError , ValueError ,OverflowError ,Account.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,'Congratulation Your Account is activated')
        return redirect('app_login:login')
    else:
        messages.error(request,'invalid activation link')
        return redirect('app_login:register')

   


#logout
@login_required(login_url='app_login:login')
def logout(request):
    auth.logout(request)
    messages.success(request,"Your are logged out")
    return redirect('app_login:login') 


#dashboard
@login_required
def dashboard(request):
    return render (request,'accounts/dashboard.html')


#forgot password
def forgotpassword(request):
    if request.method=='POST':
        email=request.POST['email']
        #jode account thake
        if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email__exact=email)#it checks that the email is exactly same or not

            #forgot pass er jnne email e msg send korar code
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Account'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_mail = EmailMessage(mail_subject, message, to=[to_email])
            send_mail.send()

            messages.success(request,'password reset has been sent your email')
            return redirect('app_login:login')

        else:
            messages.error(request,'Accounts Doesnot Exist')
            return redirect('app_login:forgot_password')
    return render(request,'accounts/forgotpassword.html')


#reset password validate
def resetpassword_validate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError , ValueError ,OverflowError ,Account.DoesNotExist):
        user=None


    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,'Please reset your password')
        return redirect('app_login:resetpassword')
    else:
        messages.error(request,'This link has been expired')
        return redirect('app_login:login')


def resetpassword(request):
    if request.method=='POST':
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']

        if password==confirm_password:
            uid=request.session.get('uid')
            user=Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'password reset successfull')
            return redirect('app_login:login')

        else:
            messages.error(request,'password doesnot match')
            return redirect('app_login:resetpassword')
    else:
        return render(request,'accounts/resetpassword.html')

    