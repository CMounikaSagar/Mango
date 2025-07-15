"""
URL configuration for mangodrf project.

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
from django.conf.urls.static import static
from category.views import *
from store.views import *
from cart.views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterUserAPIView.as_view(), name='api-register'), #accounts
    path('api/token/login/', JWTLoginAPIView.as_view(), name='jwt_login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('user_detail/', CurrentUserDetailView.as_view(), name='current-user'),
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),#category
    path('categories/<int:category_id>/', ProductsByCategoryAPIView.as_view(), name='products-by-category'),
    path('products/', ProductListCreateView.as_view(), name='product-list'),#store
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('cart/', CartAPIView.as_view(), name='cart'),#cart
    path('cart/checkout/', CheckoutAPIView.as_view(), name='checkout'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
