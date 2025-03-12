from django.urls import path
from django.views.generic import TemplateView
from . import views  # ✅ Make sure views.py is properly imported

urlpatterns = [
    path("", TemplateView.as_view(template_name="core/index.html"), name="index"),  # Home Page
    path("about/", TemplateView.as_view(template_name="core/about.html"), name="about"),  # About Page
    path("profile/", views.user_profile, name="user_profile"),  # ✅ Profile Page (linked to user_profile view)
    ]