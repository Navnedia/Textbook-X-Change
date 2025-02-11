
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path("create/", views.create_listing, name="create_listing"),
]