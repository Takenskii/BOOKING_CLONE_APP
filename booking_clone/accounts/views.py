from django.shortcuts import render, redirect
from .models import HotelUser, HotelVendor
from django.db.models import Q
from django.contrib import messages
from .utils import generateRandomToken, sendEmailToken, sendOTPtoEmail
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
import random
from django.contrib.auth.decorators import login_required

# Create your views here.

def login_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        hotel_user = HotelUser.objects.filter(email = email) 

        if not hotel_user.exists():
            messages.warning(request, "No Account Found")
            return redirect('/accounts/register/')
        
        if not hotel_user[0].is_verified:
            messages.warning(request, "Account not verified")
            return redirect('/accounts/login/')

        hotel_user = authenticate(username=hotel_user[0].username, password = password)

        if hotel_user:
            messages.success(request, "Login Success")
            login(request, hotel_user)
            return redirect('/accounts/login/')
        messages.warning(request, "Invalid Credentials")
        return redirect('/accounts/login/')

    return render(request, 'login.html')

def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')

        hotel_user = HotelUser.objects.filter(
            Q(email = email) | Q(phone_number = phone_number)
        )

        if hotel_user.exists():
            messages.warning(request, "Account already exists with Email or Phone number")
            return redirect('/accounts/login/')
        
        hotel_user = HotelUser.objects.create(
            username = phone_number,
            first_name = first_name,
            last_name = last_name,
            email = email,
            password = password,
            phone_number = phone_number,
            email_token = generateRandomToken()
        )

        hotel_user.set_password(password)
        hotel_user.save()

        sendEmailToken(email, hotel_user.email_token)

        messages.success(request, "Registration confirmation was sent to your Email")
        return redirect('/accounts/register/')
    
    return render(request, 'register.html')

def verify_email_token(request, token):
    try:
        hotel_user = HotelUser.objects.get(email_token = token)
        hotel_user.is_verified = True
        hotel_user.save()
        messages.success(request, "Email verified")
        return redirect('/accounts/login/')
    except Exception as error:
        return HttpResponse("Invalid Token")
    
def send_otp(request, email):

    hotel_user = HotelUser.objects.filter(email = email)

    if not hotel_user.exists():
        messages.warning(request, "Account not found")
        return redirect('/accounts/login/')

    otp = random.randint(1000, 9999)
    hotel_user.update(otp = otp)
    sendOTPtoEmail(email, otp)

    return redirect(f'/accounts/verify-otp/{email}/')

def verify_otp(request, email):
    if request.method == "POST":
        otp = request.POST.get('otp')
        hotel_user = HotelUser.objects.get(email=email)

        if otp == hotel_user.otp:
            messages.success(request, "Login Success")
            login(request, hotel_user)
            return redirect('/accounts/login/')
        messages.warning(request, "Wrong OTP")
        return redirect('/accounts/login/')
    
    return render(request, 'verify_otp.html')

def login_vendor(request):

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        hotel_vendor_user = HotelVendor.objects.filter(email = email) 

        if not hotel_vendor_user.exists():
            messages.warning(request, "No Account Found")
            return redirect('/accounts/register-vendor/')
        
        if not hotel_vendor_user[0].is_verified:
            messages.warning(request, "Account not verified")
            return redirect('/accounts/login-vendor/')

        hotel_vendor_user = authenticate(username=hotel_vendor_user[0].username, password = password)

        if hotel_vendor_user:
            messages.success(request, "Login Success")
            login(request, hotel_vendor_user)
            return redirect('/accounts/dashboard/')
        messages.warning(request, "Invalid Credentials")
        return redirect('/accounts/login-vendor/')

    return render(request, 'vendor/login_vendor.html')    

def register_vendor(request):

    if request.method == "POST":

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        business_name = request.POST.get('business_name')
        email_address = request.POST.get('email')
        phone_number  = request.POST.get('phone_number')
        password = request.POST.get('password')

        hotel_vendor_user = HotelVendor.objects.filter(
            Q(email = email_address) | Q(phone_number = phone_number)
        )

        if hotel_vendor_user.exists():
            messages.error(request, "Account exists with Email or Phone number")
            return redirect('/accounts/register-vendor/')

        hotel_vendor_user = HotelVendor.objects.create(
            username = phone_number,
            first_name = first_name,
            last_name = last_name,
            business_name = business_name,
            email = email_address,
            phone_number = phone_number,
            email_token = generateRandomToken()
        )

        hotel_vendor_user.set_password(password)
        hotel_vendor_user.save()

        sendEmailToken(email_address, hotel_vendor_user.email_token)

        messages.success(request, "Registration confirmation was sent to your Email")
        return redirect('/accounts/register-vendor/')
    
    return render(request, 'vendor/register_vendor.html')

@login_required(login_url='login_vendor')
def dashboard(request):
    return render(request, 'vendor/vendor_dashboard.html')

