from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path("requestbook", views.request_book, name="requestBook"),
    path("myrequests", views.my_requests, name="myrequests"),
    path("edit_request/<int:request_id>", views.edit_request, name="edit_request"),
    path("delete_request/<int:request_id>", views.delete_request, name="delete_request"),
    path("all-requests/", views.all_requests, name="all_requests")
]
