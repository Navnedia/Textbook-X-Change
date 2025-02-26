from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .forms import ListingForm, PrelistForm
from .models import Listing
from .services.autofill import PrelistSuggestionsProvider
from django.views import View

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
            return redirect("listings:dashboard") 
        else:
            print(form.errors)

    else:
        form = ListingForm(instance=autofill_data)
    return render(request, "create_listing.html", {"form": form})


def listing_page(request):
    #adding an item to the cart via POST
    if request.method == "POST":
        listing_id = request.POST.get("listing_id")
        if listing_id:
            listing_id = int(listing_id)
            cart = request.session.get("cart", [])
            if listing_id not in cart:
                cart.append(listing_id)
            request.session["cart"] = cart
        return redirect("listings:listing_page")
    #For GET requests, simply display the listings
    listings = Listing.objects.all().order_by("-id")
    return render(request, "listings.html", {"listings": listings})

def textbook_details(request, pk):
    listing = get_object_or_404(Listing, pk=pk)

    if request.method == "POST":
        listing_id = request.POST.get("listing_id")
        if listing_id:
            listing_id = int(listing_id)
            cart = request.session.get("cart", [])
            if listing_id not in cart:
                cart.append(listing_id)
            request.session["cart"] = cart
        return redirect("cart:cart")

    return render(request, "textbook_details.html", {"listing": listing})


def dashboard(request):
    listings = Listing.objects.all().order_by("-id")
    return render(request, "dashboard.html", {"listings": listings})

def edit_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect("listings:dashboard")
    else:
        form = ListingForm(instance=listing)
    return render(request, "edit_listing.html", {"form": form})

def delete_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)    
    listing.delete()
    return redirect("listings:dashboard")       
