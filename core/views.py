from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # ✅ Import Django messages framework

# ✅ User Profile View
@login_required
def user_profile(request):
    """Handles displaying and updating the user profile."""
    if request.method == "POST":
        user = request.user  # Get the logged-in user
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")

        # If user has a Profile model, update additional fields
        if hasattr(user, 'profile'):
            user.profile.phone_number = request.POST.get("phone")
            user.profile.street_address = request.POST.get("street_address")
            user.profile.city = request.POST.get("city")
            user.profile.state = request.POST.get("state")
            user.profile.zip_code = request.POST.get("zip")
            user.profile.university = request.POST.get("university")

            # Handle Profile Picture Upload
            if "profile_pic" in request.FILES:
                user.profile.profile_pic = request.FILES["profile_pic"]

        # Handle Password Change (if provided)
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if password and password == confirm_password:
            user.set_password(password)

        # Save user & profile data
        user.save()
        if hasattr(user, 'profile'):
            user.profile.save()

        messages.success(request, "Changes Successfully Made.")  # ✅ Success message added
        return redirect("user_profile")  # Redirect to prevent form resubmission

    return render(request, "core/user_profile.html")
