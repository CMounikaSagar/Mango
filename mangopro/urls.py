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
    path('',category_list,name='home'),
    path('category/<int:category_id>/', products_by_category, name='products_by_category'),
    path('cart/',cart,name="cart"),
    path('add_cart/<int:product_id>/',add_cart,name="add_cart"),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/',remove_Cart,name="remove_cart"),
    path('decreament/<int:product_id>/<int:cart_item_id>/',decreament,name="decreament"),
    path('store/',store,name="store"),
    path('checkout/',checkout,name="checkout"),
    path('place_order/',place_order,name="place_order"),
    path('place_order_1/',place_order_1,name="place_order_1"),
    path('order-complete/',order_complete,name="order_complete"),
    path('product_details/<slug:category_slug>/<slug:product_slug>/',product_detail,name='product_details'),
    path('register/',register_user,name='register'),
    path('login/',login_user,name='login'),
    path('logout/',logout_user,name='logout'),
    path('profile/',profile_view,name='profile'),
    path('edit_profile/',editprofile,name='edit_profile'),
    # path('request/', request_otp, name='request_otp'),
    # path('verify/', verify_otp, name='verify_otp'),
    
    
]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

