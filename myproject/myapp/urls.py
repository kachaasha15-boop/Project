"""
URL configuration for myproject project.

The urlpatterns list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path 
from myapp import views #==================

urlpatterns = [
    path('msg', views.msg, name='msg'), #=============
    path('msg1', views.msg1, name='msg1'),#=================
    path('about', views.about, name='about'),
    path('blog', views.blog, name='blog'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('contacts', views.contact, name='contact'),
    path('index', views.index, name='index'),
    path('services', views.services, name='services'),
    path('shop', views.shop, name='shop'),
    path('thankyou', views.thankyou, name='thankyou'),
    path('', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('Forgot_pass/', views.Forgot_pass, name='Forgot_pass'),
    path('confirm_password/', views.confirm_password, name='confirm_password'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart_plus/<int:id>', views.increment, name='increment'),
    path('cart_minus/<int:id>', views.decrement, name='decrement'),
    path('wishlists', views.wishlist, name='wishlist'),
    path('add_to_wishlist/<int:id>/', views.add_wishlist, name='add_wishlist'),
    path('wishlist/remove/<int:id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('savedetail/', views.savedetails, name='savedetails'),
    path('order_details/', views.order_details, name='order_details'),
    path('Subscribe/', views.Subscribe, name='Subscribe'),





    

]

"""
9 step 
setting.py INSTALLED_APPS---'myapp'

"""