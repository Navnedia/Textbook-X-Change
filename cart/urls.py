from django.urls import path
from django.views.generic import TemplateView
from . import views

# Declare sub-paths of /cart:
app_name = 'cart'

urlpatterns = [
    path("", TemplateView.as_view(template_name="cart/cart.html"), name="cart"), # The actual path will just be /cart.
]