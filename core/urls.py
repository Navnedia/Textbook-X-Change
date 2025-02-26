from django.urls import path
from django.views.generic import TemplateView
from . import views
from .views import home_view

urlpatterns = [
    path("", home_view, name="home"),
    path("", TemplateView.as_view(template_name="core/index.html"), name="index"),
    path("about/", TemplateView.as_view(template_name="core/about.html"), name="about"),  # About Page
]













