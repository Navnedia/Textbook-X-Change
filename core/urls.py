from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="core/index.html"), name="index"),
    path("about/", TemplateView.as_view(template_name="core/about.html"), name="about"),  # About Page
     path("profile/", TemplateView.as_view(template_name="core/user_profile.html"), name="user_profile"),  # User Profile Page
]













