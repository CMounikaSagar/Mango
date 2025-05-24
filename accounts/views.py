import requests
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
from django.conf import settings

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

def forgot_password_phone(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')  # Get the phone number from form

        try:
            user = User.objects.get(phone_number=phone)  # Check if user exists
            request.session['reset_phone'] = phone  # Store phone in session

            # Step 1: Send OTP via 2Factor
            response = requests.get(
                f"https://2factor.in/API/V1/{settings.TWO_FACTOR_API_KEY}/SMS/{phone}/AUTOGEN"
            )
            data = response.json()

            if data['Status'] == 'Success':
                request.session['session_id'] = data['Details']  # Save OTP session ID
                return redirect('verify_otp_phone')  # Redirect to OTP input page
            else:
                messages.error(request, 'OTP sending failed.')
        except User.DoesNotExist:
            messages.error(request, 'Phone number not found.')

    return render(request, 'forgot_password.html')

def verify_otp_phone(request):
    if request.method == 'POST':
        otp_input = request.POST.get('otp')  # Get OTP entered by user
        session_id = request.session.get('session_id')  # Get session ID from Step 1

        # Step 2: Verify OTP with 2Factor API
        verify_url = f"https://2factor.in/API/V1/{settings.TWO_FACTOR_API_KEY}/SMS/VERIFY/{session_id}/{otp_input}"
        response = requests.get(verify_url)
        data = response.json()

        if data['Status'] == 'Success':
            return redirect('reset_password_phone')  # Proceed to reset form
        else:
            messages.error(request, 'Invalid OTP.')
    
    return render(request, 'verify_otp.html')

def reset_password_phone(request):
    phone = request.session.get('reset_phone')  # Get phone from session
    if not phone:
        return redirect('forgot_password_phone')  # Safety check

    user = User.objects.get(phone_number=phone)  # Get user by phone

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')

        if password == confirm:
            user.set_password(password)  # Securely update password
            user.save()
            messages.success(request, 'Password reset successful.')
            return redirect('login')  # Go to login page
        else:
            messages.error(request, 'Passwords do not match.')

    return render(request, 'reset_password_phone.html')


