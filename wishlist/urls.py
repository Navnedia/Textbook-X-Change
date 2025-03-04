from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path("createwish", views.create_wish, name="request"),
    path("requestbook", views.request_book, name="requestBook"),
    path("myrequests", views.my_requests, name="myrequests"),
    path("edit_request/<int:request_id>", views.edit_request, name="edit_request"),  # Edit request URL
    path("delete_request/<int:request_id>", views.delete_request, name="delete_request"),  # Delete request URL
]