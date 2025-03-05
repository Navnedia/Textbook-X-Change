from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse
from .forms import ListingForm, PrelistForm
from .models import Listing
from .services.autofill import PrelistSuggestionsProvider
from django.contrib.auth.decorators import login_required

# Create listing views here:

# Prelist View
@login_required
def prelist(request: HttpRequest) -> HttpResponse:
    if request.POST:
        form = PrelistForm(request.POST)
        if form.is_valid():
            provider = PrelistSuggestionsProvider()
            listing = provider.process_data(isbn=form.cleaned_data["isbn"])
            
            return create_listing(request, autofill_data=listing)

    return render(request, "prelist.html", {"form": PrelistForm()})

# Create Listing View
def create_listing(request: HttpRequest, autofill_data: Listing | None = None) -> HttpResponse:
    if not autofill_data and request.method == "POST":
        form = ListingForm(request.POST, request.FILES)    
        if form.is_valid():
            form.save()
            return redirect("dashboard:dashboard") 
        else:
            print(form.errors)

    else:
        form = ListingForm(instance=autofill_data)
    return render(request, "create_listing.html", {"form": form})

# Listing Page with Filtering
def listing_page(request):
    # Adding an item to the cart via POST
    if request.method == "POST":
        listing_id = request.POST.get("listing_id")
        if listing_id:
            listing_id = int(listing_id)
            cart = request.session.get("cart", [])
            if listing_id not in cart:
                cart.append(listing_id)
            request.session["cart"] = cart
        return redirect("listings:listing_page")
    
    # For GET requests, simply display listings with selected filters:
    query = request.GET.get("q", "").strip()
    location_filter = request.GET.get("location", "All")

    # Filter listings based on search query
    listings = Listing.objects.all()
    if query:
        listings = listings.filter(title__icontains=query)  # Filter by title containing search term

    # Apply location filter
    if location_filter == "Global":
        listings = Listing.objects.filter(location="Global").order_by("-id")
    elif location_filter == "Local":
        listings = Listing.objects.filter(location="Local").order_by("-id")
    else:
        listings = Listing.objects.all().order_by("-id")  # Default: Show all listings

    # Order results by newest first
    listings = listings.order_by("-id")

    return render(request, "listings.html", {
        "listings": listings,
        "location_filter": location_filter,
        "query": query  # Pass query to template for display
    })

# Textbook Details View
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


def edit_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect("dashboard:dashboard")
    else:
        form = ListingForm(instance=listing)
    return render(request, "edit_listing.html", {"form": form})

@login_required
def delete_listing(request: HttpRequest, listing_id) -> HttpResponse:
    try:
        listing = Listing.objects.get(pk=listing_id)
        listing.delete()
    finally:
        return redirect("dashboard:dashboard")

