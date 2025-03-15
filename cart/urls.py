from django.urls import path
from django.views.generic import TemplateView
from . import views

# Declare sub-paths of /cart:
app_name = 'cart'

urlpatterns = [
    path("", views.cart_view, name="cart"), # The actual path will just be /cart.
    path("checkout/<int:listing_id>/", views.checkout_view, name="checkout"),
    path("order-confirmation/<int:order_id>/", views.order_confirmation_view, name="order_confirmation"),
]