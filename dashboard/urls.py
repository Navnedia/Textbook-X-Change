from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("confirm_shipment/<int:order_id>/", views.confirm_shipment, name="confirm_shipment"),
]
