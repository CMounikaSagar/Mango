"""
URL configuration for mangopro project.

The `urlpatterns` list routes URLs to views. For more information please see:
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
from accounts.views import *
from mangoapp.views import *
from category.views import *
from store.views import *
from orders.views import *
from cart.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import HttpResponse

# def hello(request):
#     return HttpResponse('Hellooo')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',category_list,name='home'),#category
    path('home',category_list,name='home'),#category
    path('category/<int:category_id>/', products_by_category, name='products_by_category'),#category
    path('cart/',cart,name="cart"),#cart
    path('add_cart/<int:product_id>/',add_cart,name="add_cart"),#cart
    path('remove_cart/<int:product_id>/<int:cart_item_id>/',remove_Cart,name="remove_cart"),#cart
    path('decreament/<int:product_id>/<int:cart_item_id>/',decreament,name="decreament"),#cart
    path('store/',store,name="store"),#store
    path('add_wishlist/<int:product_id>/', add_to_wishlist, name='add_wishlist'),#store
    path('remove_wishlist/<int:product_id>/', remove_wishlist, name='remove_wishlist'),#store
    path('wishlist/', wishlist_view, name='wishlist'),#store
    path('checkout/',checkout,name="checkout"),#cart
    path('place_order/',place_order,name="place_order"),#orders
    path('place_order_1/',place_order_1,name="place_order_1"),#orders
    path('order-complete/',order_complete,name="order_complete"),#orders
    path('product_details/<slug:category_slug>/<slug:product_slug>/',product_detail,name='product_details'),#store
    path('register/',register_user,name='register'),#accounts
    path('login/',login_user,name='login'),#accounts
    path('logout/',logout_user,name='logout'),#accounts
    path('profile/',dashboard,name='profile'),
    path('edit_profile/',editprofile,name='edit_profile'),
    path('myorders/',myorders,name='myorders'),
    # path('wishlist/<int:category_id>/',toggle_wishlist,name='wishlist'),
    # path('request/', request_otp, name='request_otp'),
    # path('verify/', verify_otp, name='verify_otp'),
    
    
]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

