
from django.contrib import admin
from django.urls import include, path
from . import views
from .views import EbayPriceScraperView
app_name = 'listings'
urlpatterns = [
    path("create/", views.create_listing, name="create_listing"),
    path("fetch_ebay_price/", EbayPriceScraperView.as_view(), name="fetch_ebay_price"),
]