from django.urls import path
from . import views

app_name = 'pricing_engine'

urlpatterns = [
    path("suggest/", views.EbayPriceScraperView.as_view(), name="get_suggestions"),
]
