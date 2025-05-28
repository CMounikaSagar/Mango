from django.shortcuts import render,redirect,get_object_or_404
from accounts.forms import *
from category.models import *
from orders.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login')
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id = request.user.id , is_ordered = True)
    orders_count = orders.count()
    user_profile = User_Profile_Model.objects.get(user_id=request.user.id)
    context = {
        'orders_count' : orders_count,
        'user_profile' : user_profile
    }
    return render(request,'profilePage.html',context)

def myorders(request):
    orders= Order.objects.filter(user = request.user,is_ordered = True).order_by('-created_at')
    context = {
        'orders':orders
    }
    print(orders)
    return render(request,'my_orders.html',context)