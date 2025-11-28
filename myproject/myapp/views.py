
from django.shortcuts import render, redirect, HttpResponse
from .models import *
import random
from django.core.mail import send_mail
from django.utils.timezone import now
import razorpay



# Create your views here.
def msg(request):
    return HttpResponse("Hello Python")


def msg1(request):
    return HttpResponse("Hello Python 1")


def about(request):
    return render(request,"about.html")

def blog(request):
    return render(request,"blog.html")

def checkout(request):
    uid = user.objects.get(name=request.session['name'])        

    order_items = CartItem.objects.filter(user=uid, is_active=True)
    total = sum(item.product.price * item.quantity for item in order_items)
    if total > 0:
        amount = total*100 #100 here means 1 dollar,1 rupree if currency INR
        client = razorpay.Client(auth=('rzp_test_bilBagOBVTi4lE','77yKq3N9Wul97JVQcjtIVB5z'))
        response = client.order.create({'amount':amount,'currency':'INR','payment_capture':1})
        context = {
            'order_items': order_items,
            'total': total,
            'response':response,
        }
    else:
        context = {
            'order_items': order_items,
            'total': total,
        }
    return render(request, "checkout.html",context)

def savedetails(request):
    if request.method == 'POST':
        country = request.POST.get('country')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        company_name = request.POST.get('company_name')
        address = request.POST.get('address')
        state_country = request.POST.get('state_country')
        email_address = request.POST.get('email_address')
        phone = request.POST.get('phone')

        checkout_address = CheckoutDetails.objects.create(
            country=country,
            first_name=first_name,
            last_name=last_name,
            company_name=company_name,
            address=address,
            state_country=state_country,
            email_address=email_address,
            phone=phone
        )
        uid = user.objects.get(name=request.session['name'])
        cart_items = CartItem.objects.filter(user=uid,is_active=True)
        for item in cart_items:
            quantity = item.quantity
            subtotal = item.product.price * quantity
            total = subtotal
            amount = total*100  
            client = razorpay.Client(auth=('rzp_test_bilBagOBVTi4lE','77yKq3N9Wul97JVQcjtIVB5z'))
            response = client.order.create({'amount':amount,'currency':'INR','payment_capture':1})

            Order.objects.create(
                user=uid,
                address=checkout_address,
                product=item.product,
                quantity=item.quantity, 
                subtotal=subtotal,
                total=total,
                date=now()
            )
            cart_items = CartItem.objects.filter(user=uid,is_active=True).update(is_active=False)

        return redirect('thankyou')

    return render(request, "checkout.html")





def contact(request):
    if request.POST:
        f_name=request.POST['f_name']
        l_name=request.POST['l_name']
        e_address=request.POST['e_address']
        message=request.POST['message'] 
        print(f_name,l_name,e_address,message) 
        contacts.objects.create(f_name=f_name,l_name=l_name,e_address=e_address,message=message)  
    return render(request,"contact.html")


# def index(request):
#     products = Product.objects.all()[:3] 
#     return render(request, 'index.html', {'products': products})

def index(request):
    products = Product.objects.all()[:3]
    
    # Cart logic (assuming cart is stored in session as a dict of item_id: quantity)
    cart = request.session.get('cart', {})
    cart_item_count = sum(cart.values())  # Total quantity of all items

    return render(request, 'index.html', {
        'products': products,
        'cart_item_count': cart_item_count,
    })

def services(request):
    return render(request,"services.html")

def thankyou(request):
    return render(request,"thankyou.html")


def register(request):
    if request.POST:
        name=request.POST['name']
        email=request.POST['email']
        password1=request.POST['password']
        password2=request.POST['confirm_password']
        print(name,email,password1,password2)
        uid=user.objects.filter(email=email).exists()
        user_uid=user.objects.filter(name=name).exists()
        print(uid)
        if user_uid:
            contaxt={
                "msg":"name already exist"
            }
            return render(request, 'register.html',contaxt)
        elif uid:
            contaxt={
                "msg":"Email already registered"
            }
            return render(request, 'register.html',contaxt)
        else:
            if password1 == password2:
                user.objects.create(name=name,email=email,password=password1)
                return redirect('login')  

            else:
                contaxt={
                    "msg":"Password Not match"
                }
                return render(request, 'register.html',contaxt)
    return render(request, 'register.html')

def login(request):
    if "name" in request.session:
        return redirect(index)
    else:
        if request.POST:
            name=request.POST['username']
            password=request.POST['password']
            print(name,password)
            user_uid=user.objects.filter(name=name).exists()
            if user_uid:
                user_uid=user.objects.get(name=name)
                if user_uid.password == password:
                    request.session["name"]=user_uid.name
                    return redirect(index)
                else:
                    contaxt={
                            "msg":"Incorrect password"
                        }
                    return render(request,"login.html",contaxt)
            else:
                contaxt={
                        "msg":"User Not exists"
                    }
                return render(request,"login.html",contaxt)
    return render(request,"login.html")

def logout(request):
    del request.session['name']
    return redirect(login)

def profile(request):
    uid=user.objects.get(name=request.session['name'])
    print(uid)
    if request.POST:
        name=request.POST['name']
        email=request.POST['email']
        phone_number=request.POST['phone_number']
        if request.FILES:
            image=request.FILES['image']
            uid.name=name
            uid.email=email
            uid.phone_number=phone_number
            uid.image=image
            uid.save()
        else:
            uid.name=name
            uid.email=email
            uid.phone_number=phone_number
            uid.save()
        request.session["name"]=uid.name
    con={
        "uid":uid
    }
    return render(request, 'profile.html',con)

def Forgot_pass(request):
    if request.POST:
        email=request.POST['email']
        otp=random.randint(1000,9999)
        print(email)
        uid=user.objects.filter(email=email).exists()
        if uid:
            send_mail(" Reset password",f"Your OTP for reset password is: {otp}","kachaasha15@gmail.com",[email])
            uid=user.objects.get(email=email)
            uid.otp=otp
            uid.save()
            con={
                "uid":uid
            }
            return render(request, 'confirm_password.html',con)
        else:
            con={
                "msg":"Invalid Email"
            }
            return render(request, 'Forgot_pass.html',con)

    return render(request, 'Forgot_pass.html')


def confirm_password(request):
    if request.method == 'POST':
        email=request.POST['email']
        otp=request.POST['otp']
        new_password=request.POST['new_password']
        confirm_password1=request.POST['confirm_password']
        print(email,otp,new_password,confirm_password)
        uid=user.objects.get(email=email)
        print(type(uid.otp),type(otp))
        if uid.otp == int(otp):
            print("okokok")
            if new_password == confirm_password1:
                uid.password=new_password
                uid.save()
                return redirect(login)
            else:
                contaxt={
                    "msg":"Password Not match",
                    "uid":uid
                }
                return render(request, 'confirm_password.html',contaxt)
        else:
            contaxt={
                "msg":"Invalid OTP",
                "uid":uid
            }
            return render(request, 'confirm_password.html',contaxt)    
    else:
        return render(request,"confirm_password.html")


def shop(request):
    products = Product.objects.all()
    wishlist_products = []
    uid = user.objects.get(name=request.session['name'])
    wishlist_items = wishlistItem.objects.filter(user=uid)
    wishlist_products = [item.product.id for item in wishlist_items]

    return render(request, 'shop.html', {
        'products': products,
        'wishlist_products': wishlist_products
    })




def cart(request):
    uid=user.objects.get(name=request.session['name'])
    cart_items = CartItem.objects.filter(user=uid, is_active=True)  # You should filter by session/user
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'cart.html', context)

def remove_from_cart(request, item_id):
    item = CartItem.objects.get(id=item_id)
    item.delete()
    return redirect('cart')


def add_to_cart(request, product_id):
    uid=user.objects.get(name=request.session['name'])
    pid = Product.objects.get(id=product_id)
    cart_item = CartItem.objects.filter(user=uid,product=pid, is_active=True).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.total = cart_item.quantity * pid.price
        cart_item.is_active=True
        cart_item.save()
    else:
        CartItem.objects.create(user=uid,product=pid, quantity=1, total=pid.price)

    return redirect('cart')

def increment(request,id):
    cid=CartItem.objects.get(id=id)
    cid.quantity += 1
    cid.total=cid.product.price * cid.quantity
    cid.save()
    return redirect('cart')


def decrement(request,id):
    cid=CartItem.objects.get(id=id)
    if cid.quantity > 1:
        cid.quantity -= 1
        cid.total=cid.product.price * cid.quantity
        cid.save()
    else:
        cid.delete()
    return redirect('cart')

def wishlist(request):
    wid=user.objects.get(name=request.session['name'])
    wishlist_items = wishlistItem.objects.filter(user=wid) 

    context = {
        'wishlist_items': wishlist_items
    }
    return render(request, 'wishlist.html', context)

def add_wishlist(request,id):
    uid=user.objects.get(name=request.session['name'])
    pid = Product.objects.get(id=id)
    wishlist_item = wishlistItem.objects.filter(user=uid,product=pid).first()

    wishlist_in = wishlistItem.objects.filter(user=uid, product=pid)
    if wishlist_in.exists():
        wishlist_in.delete()  
    else:
        wishlistItem.objects.create(user=uid, product=pid)
    return redirect('wishlist')

def remove_from_wishlist(request,id):
    item = wishlistItem.objects.get(id=id)
    item.delete()
    return redirect('wishlist')

def remove_from_(request, item_id):
    item = wishlistItem.objects.get(id=item_id)
    item.delete()
    return redirect('wishlist')

def order_details(request):
    uid = user.objects.get(name=request.session['name'])  
    orders = Order.objects.filter(user=uid)

    context = {
        'orders': orders
    }
    return render(request, 'order_details.html', context)

def Subscribe(request):
    if request.POST:
        name=request.POST['name']
        email=request.POST['email']
        Subscribes.objects.create(name=name,email=email)

    return render(request, 'index.html')




        


