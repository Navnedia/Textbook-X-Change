from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .forms import ListingForm, PrelistForm
from .models import Listing
from .services.autofill import PrelistSuggestionsProvider

# Create listing views here:

def prelist(request: HttpRequest) -> HttpResponse:
    if request.POST:
        form = PrelistForm(request.POST)
        if form.is_valid():
            provider = PrelistSuggestionsProvider()
            listing = provider.process_data(isbn=form.cleaned_data["isbn"])
            
            return create_listing(request, autofill_data=listing)

    return render(request, "prelist.html", {"form": PrelistForm()})


def create_listing(request: HttpRequest, autofill_data: Listing | None = None) -> HttpResponse:
    if not autofill_data and request.method == "POST":
        form = ListingForm(request.POST, request.FILES)    
        if form.is_valid():
            form.save()
            return redirect("listings:listing_page") 
        else:
            print(form.errors)

    else:
        form = ListingForm(instance=autofill_data)
    return render(request, "create_listing.html", {"form": form})


def listing_page(request):
    listings = Listing.objects.all().order_by("-id")  
    return render(request, "listings.html", {"listings": listings})
