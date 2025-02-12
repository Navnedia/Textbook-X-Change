from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required



def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("home")  # Ensure "home" exists in urls.py
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request, "Passwords do not match")
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            login(request, user)  # Log in user automatically
            messages.success(request, "Account created successfully")
            return redirect("home")  # Redirect to home page after registration

    return render(request, "register.html")

def forgot_password_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        messages.success(request, "If this email exists, you will receive a password reset link.")
        return redirect("login")

    return render(request, "forgot_password.html")

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")
