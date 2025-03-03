from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path("createwish", views.create_wish, name="request"),
    path("requestbook", views.request_book, name="requestBook"),
    
]