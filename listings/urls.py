
from django.urls import path
from . import views
from .views import EbayPriceScraperView

app_name = 'listings'

urlpatterns = [
    path("", views.listing_page, name="listing_page"),
    path("prelist/", views.prelist, name="prelist"),
    path("create/", views.create_listing, name="create_listing"),
    path("fetch_ebay_price/", EbayPriceScraperView.as_view(), name="fetch_ebay_price"),
    path("<int:pk>/", views.textbook_details, name="textbook_details"),


]
