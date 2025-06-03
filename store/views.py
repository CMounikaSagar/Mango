from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from category.models import *
from cart.models import *
from cart.views import _cart_id
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator

# Create your views here.
def store(request,category_slug = None):
    categories = None
    products = None
    wishlist_items=[]
    
    if category_slug != None:
        categories = get_object_or_404(Category,slug=category_slug)
        products = Product.objects.filter(category = categories,is_available = True)
        product_count = Product.objects.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        paginator = Paginator(products, 8)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        product_count = Product.objects.count()
        colors = ["bg-orange-100", "bg-green-100", "bg-blue-100", "bg-yellow-100", "bg-pink-100","bg-red-100","bg-purple-100","bg-indigo-100"]
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
    context = {
        'products':paged_product,
        'product_count':product_count,
        'colors':colors,
        'wishlist_items':wishlist_items
        
    }
    return render(request,'store.html',context)

def product_detail(request,category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug = category_slug,slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request),product = single_product).exists()
        
    except Exception as e:
        raise e 
    
    context = {
        'single_product':single_product,
        'in_cart':in_cart
    }
    return render(request,'product_details.html',context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            product = Product.objects.order_by('-created_date').filter(Q(Product_name__icontains = keyword) | Q(slug__icontains = keyword))
            product_count = Product.objects.count()
            colors = ["bg-orange-100", "bg-green-100", "bg-blue-100", "bg-yellow-100", "bg-pink-100","bg-red-100","bg-purple-100","bg-indigo-100"]
            search_item= zip(product, colors * (len(product) // len(colors) + 1))
        if request.user.is_authenticated:
            wishlist_items = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
            
    context = {
        'products':search_item,
        'product_count':product_count,
        'wishlist_items':wishlist_items
    }
            
    return render(request,'search.html',context)

@login_required(login_url="login")
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect(request.META.get('HTTP_REFERER', '/store/'))

def remove_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist_object = get_object_or_404(Wishlist,user=request.user, product=product)
    Wishlist_object.delete()
    return redirect(request.META.get('HTTP_REFERER'))  

@login_required(login_url='login')
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    wishlist_count = Wishlist.objects.count()
    colors = ["bg-orange-100", "bg-green-100", "bg-blue-100", "bg-yellow-100", "bg-pink-100","bg-red-100","bg-purple-100","bg-indigo-100"]
    wishlist_item= zip(wishlist_items, colors * (len(wishlist_items) // len(colors) + 1))
    context = {
        'wishlist_item':wishlist_item,
        # 'wishlist_count':wishlist_count,
    }
    return render(request, 'wishlist.html', context)