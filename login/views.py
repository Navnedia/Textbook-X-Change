from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse
from django.http import HttpResponseRedirect


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("index")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        # Email format validation
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(email_regex, email):
            messages.error(request, "Invalid email format.")
            return render(request, "register.html", {"email_error": "Invalid email format."})

        # Password match validation
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "register.html", {"password_error": "Passwords do not match."})

        # Check if username is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken. Choose a different one.")
            return render(request, "register.html", {"username_error": "Username is already taken."})

        # Check if email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, "register.html", {"email_error": "An account with this email already exists."})

        # Create user if all checks pass
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Account created successfully! You can now log in.")
        return redirect("login")

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

def custom_password_reset_confirm(request, uidb64, token):
    """Handles password reset confirmation and redirects to login on success."""
    view = PasswordResetConfirmView.as_view(
        template_name="create_new_password.html"
    )
    
    response = view(request, uidb64=uidb64, token=token)

    # If the form submission was successful, explicitly redirect to login
    if request.method == "POST" and response.status_code == 200:
        return HttpResponseRedirect(reverse("login"))

    return response