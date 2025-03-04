from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path("", views.listing_page, name="listing_page"),
    path("<int:pk>/", views.textbook_details, name="textbook_details"),
    path("prelist/", views.prelist, name="prelist"),
    path("create/", views.create_listing, name="create_listing"),
    path("edit/<int:listing_id>/", views.edit_listing, name="edit_listing"),
    path("search/", views.search_results, name="search_results"),
    path("delete/<int:listing_id>/", views.delete_listing, name="delete_listing")
]
