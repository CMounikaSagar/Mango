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


# def profile_view(request):
#     userprofile = get_object_or_404(User_Profile_Model,user = request.user)
#     if request.method == 'POST':
#         if request.user.is_authenticated:
#             orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
#             user_form = UserForm(request.POST,instance=request.user)
#             profile_form = UserProfileForm(request.POST,request.FILES,instance=userprofile)
#             if user_form.is_valid() and profile_form.is_valid():
#                 user_form.save()
#                 profile_form.save()
#                 print("Saved profile image:", profile_form.cleaned_data.get('profile_picture'))
#                 messages.success(request,'Your profile has been update')
#                 return redirect('edit_profile')
#     else:
#         user_form = UserForm(instance=request.user)
#         profile_form = UserProfileForm(instance=userprofile)
#     if request.user.is_authenticated:
#         orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
#     context = {
#         'user_form' : user_form,
#         'profile_form' :profile_form,
#         'user_profile' : userprofile,
#         'orders':orders
#     }
#     return render(request, 'profilePage.html', context)
   

    # return render(request,'profilePage.html')

