from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from cart.views import _cart_id
from orders.models import *
from cart.models import *
from accounts.forms import *
from accounts.models import *
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
def index(request):
    return render(request,'index.html')


def login_user(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        # Check if phone number exists
        if not User.objects.filter(phone_number=phone).exists():
            messages.error(request, "Phone number not found. Please register.")
            return redirect('register')

        user = authenticate(request, username=phone, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # or your actual home route
        else:
            messages.error(request, "Invalid phone number or password.")
            return redirect('login')
    return render(request, 'login.html')



def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # print('form is valid')
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = Account.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                email = email,
                username = username,
                password = password,
                phone_number = phone_number
            )
            user.save()
            
            #Automatic user creation
            
            profile = User_Profile_Model()
            profile.user_id = user.id
            profile.profile_picture = 'default/default-user.png'
            profile.save()
            
            
            return render(request,'login.html')
           
        else:
            print(form.errors)
        
    else:
        form = RegistrationForm()
    return render(request,'register.html',{'form':form})

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    messages.success(request,'logout successfully')
    return redirect('login')

def editprofile(request):
    userprofile = get_object_or_404(User_Profile_Model,user = request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST,instance=request.user)
        profile_form = UserProfileForm(request.POST,request.FILES,instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Your profile has been update')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form' : user_form,
        'profile_form' :profile_form,
        'user_profile' : userprofile
    }
    return render(request,'edit_profile.html',context)