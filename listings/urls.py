from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path("", views.listing_page, name="listing_page"),
    path("prelist/", views.prelist, name="prelist"),
    path("create/", views.create_listing, name="create_listing"),
]
