from django.shortcuts import render,redirect,get_object_or_404
from.models import *
from store.models import *

# Register your models here.



def category_list(request):
    categories = Category.objects.all()
    products = Product.objects.select_related('category')
    colors = ["bg-orange-100", "bg-green-100", "bg-blue-100", "bg-yellow-100", "bg-pink-100"]
    category_data = zip(categories, colors * (len(categories) // len(colors) + 1))
    # print(categories)
    return render(request, 'index.html', {'category_data': category_data,'products':products})

def products_by_category(request,category_id):
    category = get_object_or_404(Category,id=category_id)
    products = Product.objects.filter(category=category)
    colors = ["bg-orange-100", "bg-green-100", "bg-blue-100", "bg-yellow-100", "bg-pink-100"]
    product_data= zip(products, colors * (len(products) // len(colors) + 1))
    context = {
        'category':category,
        'products':product_data,
    }
    return render(request,'products_by_category.html',context)
