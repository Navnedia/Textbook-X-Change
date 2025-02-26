
from django.urls import path
from . import views
from .views import EbayPriceScraperView

app_name = 'listings'

urlpatterns = [
    path("", views.listing_page, name="listing_page"),
    path("<int:pk>/", views.textbook_details, name="textbook_details"),
    path("prelist/", views.prelist, name="prelist"),
    path("create/", views.create_listing, name="create_listing"),
    path("fetch_ebay_price/", EbayPriceScraperView.as_view(), name="fetch_ebay_price"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("listing/edit/<int:listing_id>/", views.edit_listing, name="edit_listing"),
    path("listing/delete/<int:listing_id>/", views.delete_listing, name="delete_listing")
]
