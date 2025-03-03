from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse
from listings.models import Listing

# Define dashboard related views here:


def dashboard(request: HttpRequest) -> HttpResponse:
    listings = Listing.objects.all().order_by("-id")
    return render(request, "dashboard/dashboard.html", {"listings": listings})
