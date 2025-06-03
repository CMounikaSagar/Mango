import requests
from django.shortcuts import render,redirect,get_object_or_404
# from django.utils.http import url_has_allowed_host_and_scheme
from .models import *
from mangoapp.models import *
from cart.views import _cart_id
from orders.models import *
from cart.models import *
from accounts.forms import *
from accounts.models import *
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
import random
from django.conf import settings
from .decorators import *
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
def index(request):
    return render(request,'index.html')

@unauthenticated_user
def login_user(request):
    next_url = request.POST.get('next') or request.GET.get('next') or 'home'

    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        if not User.objects.filter(phone_number=phone).exists():
            messages.error(request, "Phone number not found. Please register.")
            return redirect('register')

        user = authenticate(request, username=phone, password=password)
        if user is not None:
            login(request, user)
            print("GET next:", request.GET.get('next'))
            print("POST next:", request.POST.get('next'))
            # if next_url and url_has_allowed_host_and_scheme(next_url, settings.ALLOWED_HOSTS):
            return redirect(next_url)
        else:
            messages.error(request, "Invalid phone number or password.")
            return redirect(f"{reverse('login')}?next={next_url}")

    return render(request, 'login.html', {'next': next_url})


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
    # messages.success(request,'logout successfully')
    return redirect('login')

def editprofile(request):
    userprofile = get_object_or_404(User_Profile_Model,user = request.user)
    if request.method == 'POST':
        print("FILES:", request.FILES)
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

def forgot_password_request(request):
    if request.method == 'POST':
        phone = request.POST.get('phone', '').strip()
        normalized_phone = phone[-10:]  # take last 10 digits
        print("User entered phone:", phone)
        print("Normalized phone:", normalized_phone)

        try:
            user = User.objects.get(phone_number=phone)
            print(user)
            otp = str(random.randint(1000, 9999))

            # Save OTP
            OTP.objects.create(phone_number=phone, otp_code=otp)

            # Simulate sending OTP (log it or show on screen)
            print(f"OTP for {phone} is {otp}")  # Use logging in real apps
            request.session['phone'] = phone
            messages.info(request, f"OTP sent to {phone}. (Simulated)")

            return redirect('verify_otp')
        except User.DoesNotExist:
            messages.error(request, "Phone number not found.")
    return render(request, 'forgot_password.html')


def verify_otp(request):
    if request.method == 'POST':
        otp1 = request.POST.get('otp1')
        otp2 = request.POST.get('otp2')
        otp3 = request.POST.get('otp3')
        otp4 = request.POST.get('otp4')
        # otp5 = request.POST.get('otp5')
        # otp6 = request.POST.get('otp6')

        entered_otp = f"{otp1}{otp2}{otp3}{otp4}"
        phone = request.session.get('phone')

        try:
            otp_entry = OTP.objects.filter(phone_number=phone).latest('created_at')
            if otp_entry.otp_code == entered_otp and otp_entry.is_valid():
                request.session['otp_verified'] = True
                return redirect('reset_password')
            else:
                messages.error(request, "Invalid or expired OTP.")
        except OTP.DoesNotExist:
            messages.error(request, "OTP not found.")
    return render(request, 'verify_otp.html')


def reset_password(request):
    if not request.session.get('otp_verified'):
        return redirect('forgot_password')

    if request.method == 'POST':
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            phone = request.session.get('phone')
            user = User.objects.get(phone_number=phone)
            user.password = make_password(new_password)
            user.save()

            # Clear session
            request.session.flush()
            messages.success(request, "Password reset successful.")
            return redirect('login')
    return render(request, 'reset_password.html')

def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']
        
        user = Account.objects.get(username__exact = request.user.username)
        
        if new_password == confirm_new_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password) 
                user.save()
                messages.success(request,'Password Updated successfull')
                return redirect('change_password')
            else:
                messages.error(request,'please enter valid current password')
    return render(request,'change_password.html')