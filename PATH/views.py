from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Authenticate user
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Log in the user
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('home')  # Replace 'home' with the name of your home view
        else:
            messages.error(request, 'Invalid login credentials. Please try again.')

    return render(request, 'PATH/login.html')  # Replace 'login.html' with the name of your login template

@login_required
def home(request):
    # Your home view logic goes here
    return render(request, 'PATH/home.html')  # Replace 'home.html' with the name of your home template

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after registration
            return redirect('home')  # Redirect to home or any other desired page
    else:
        form = UserCreationForm()
    return render(request, 'PATH/register.html', {'form': form})