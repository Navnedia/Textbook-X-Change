from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # ✅ Import Django messages framework

# ✅ User Profile View
@login_required
def user_profile(request):
    """Handles displaying and updating the user profile."""
    user = request.user
    # Ensure profile exists
    if hasattr(user, "profile"):
        profile = user.profile
    else:
        profile = None  # If profile does not exist, avoid errors

    if request.method == "POST":
        # Process the full_name input by splitting it into first and last name.
        full_name = request.POST.get("full_name")
        if full_name:
            name_parts = full_name.split(" ", 1)
            user.first_name = name_parts[0]
            user.last_name = name_parts[1] if len(name_parts) > 1 else ""

        user.username = request.POST.get("username")
        user.email = request.POST.get("email")

        # Ensure profile fields update correctly
        if profile:
            # ✅ Save the uploaded profile picture
            if "profile_pic" in request.FILES and profile:
                profile.profile_pic = request.FILES["profile_pic"]
            profile.save()  # Save profile changes

        user.save()  # Save user changes

        messages.success(request, "Changes Successfully Made.")
        return redirect("user_profile")

    return render(request, "core/user_profile.html", {"user": user, "profile": profile})
