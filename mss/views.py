from django.forms import model_to_dict
from django.shortcuts import render,redirect
from user.models import User,UserOTPTable
from admincf.models import adminmusic
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from datetime import date
from .utils import generate_otp,verify_otp
from django.core.mail import send_mail
from django.conf import settings
def model_to_dict_serializable(instance):
    """Convert a model instance to a dictionary, handling date and image fields."""
    data = model_to_dict(instance)
    for key, value in data.items():
        if isinstance(value, date):
            # Convert date objects to ISO format strings
            data[key] = value.isoformat()
        elif hasattr(value, 'url'):
            # Convert ImageFieldFile or FileFieldFile to their URL or path
            data[key] = value.url  # Use the file's URL
    return data
def index(request):
    
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if the user is an admin
        try:
            admin = adminmusic.objects.get(username=username, password=password)
            # Here you can add any session or authentication logic for admin
            # messages.success(request, 'Admin login successful!')
            request.session['admin'] = model_to_dict(admin)
            return redirect('admin_dashboard')  # Redirect to admin dashboard
        except adminmusic.DoesNotExist:
            pass
        
        # Check if the user is a regular user
        try:
            user = User.objects.get(username=username, password=password)
            # Here you can add any session or authentication logic for regular users
            # messages.success(request, 'User login successful!')
            request.session['user'] = model_to_dict_serializable(user)
            return redirect('user_dashboard')  # Redirect to user dashboard
        except User.DoesNotExist:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        pincode = request.POST['pincode']
        dob = request.POST['dob']

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register')
        if User.objects.filter(phone=phone).exists():
            messages.error(request, 'Phone number already exists.')
            return redirect('register')

        # Create a new user
        user = User(
            username=username,
            password=password,  
            name=name,
            email=email,
            phone=phone,
            city=city,
            state=state,
            country=country,
            pincode=pincode,
            dob=dob
        )
        user.save()

        # messages.success(request, 'Registration successful!')
        request.session['user'] = model_to_dict_serializable(user)
        return redirect('user_dashboard')

    return render(request, 'register.html')

def login_with_send_otp(request):
    if request.method == 'POST':
        user_email = request.POST.get('user_email')
        user = User.objects.get(email=user_email)
        if not user:
            messages.error(request, 'User not found')
            return redirect('login')
        otp = generate_otp()
        userotp = UserOTPTable(user_email,otp)
        
        send_mail(
            'OTP for login',
            f'Your OTP is {otp}',
            settings.EMAIL_HOST_USER,
            [user_email],
            fail_silently=False,
        )
        userotp.save()
    
    return render(request, 'login_with_otp.html')
        
# Create your views here.
