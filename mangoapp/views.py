from django.shortcuts import render,redirect,get_object_or_404
from accounts.forms import *
from category.models import *
from orders.models import *
from django.contrib import messages

# Create your views here.

def profile_view(request):
    userprofile = get_object_or_404(User_Profile_Model,user = request.user)
    if request.method == 'POST':
        if request.user.is_authenticated:
            orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
            user_form = UserForm(request.POST,instance=request.user)
            profile_form = UserProfileForm(request.POST,request.FILES,instance=userprofile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                print("Saved profile image:", profile_form.cleaned_data.get('profile_picture'))
                messages.success(request,'Your profile has been update')
                return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'user_form' : user_form,
        'profile_form' :profile_form,
        'user_profile' : userprofile,
        'orders':orders
    }
    return render(request, 'profilePage.html', context)
   

    # return render(request,'profilePage.html')

