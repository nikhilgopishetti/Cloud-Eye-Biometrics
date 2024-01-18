from django.shortcuts import render, redirect
from django.contrib import messages
from validate_email import validate_email
from django.contrib.auth.models import User
from .utils import generate_token, send_activation_email, activate_user
from django.contrib.auth import authenticate, login, logout

def create_staff_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # Create a staff user
        user = User.objects.create_user(username=username, email=email, password=password, is_staff=True)

        messages.success(request, f'Staff user {username} created successfully!')
        return redirect('home')  # Redirect to home or another appropriate URL

    return render(request, 'main/createstaffuser.html') 

def create_superuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # Check if a user with the given username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Try another username.')
            return redirect('create_superuser')  # Redirect to the same page

        # Create a superuser
        user = User.objects.create_superuser(username=username, email=email, password=password)

        messages.success(request, f'Superuser {username} has been created successfully!')
        return redirect('home')  # Redirect to the home page or admin panel

    return render(request, 'main/createsuperuser.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('main-home')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'main/login.html')


def register(request):
    if request.method == "POST":
        context = {'has_error': False, 'data': request.POST}
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if len(password) < 6:
            messages.add_message(request, messages.ERROR, 'Password should be at least 6 characters')
            context['has_error'] = True

        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR, 'Username is taken, choose another one')
            context['has_error'] = True

        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR, 'Email is taken, choose another one')
            context['has_error'] = True

        if context['has_error']:
            return render(request, 'main/register.html', context)

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save()

        send_activation_email(user, request)

        messages.add_message(request, messages.SUCCESS, 'We sent you an email to verify your account')

    return render(request, 'main/register.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request, 'main/home.html')


def employee_home_view(request):
    return render(request, 'employeewebsite/home.html')

