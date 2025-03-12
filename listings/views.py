from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse
from .forms import ListingForm, PrelistForm, SearchForm, FileFieldForm, MultipleFileField, MultipleFileInput
from .models import Listing, ListingImage
from django.db.models import Q
from .services.autofill import PrelistSuggestionsProvider
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create listing views here:

def user_profile(request):
    return render(request, 'user_profile.html')

# Prelist View
@login_required
def prelist(request: HttpRequest) -> HttpResponse:
    if request.GET:
        form = PrelistForm(request.GET)
        if form.is_valid():
            provider = PrelistSuggestionsProvider()
            listing = provider.process_data(isbn=form.cleaned_data["isbn"])
            
            return create_listing(request, autofill_data=listing)

    return render(request, "prelist.html", {"form": PrelistForm()})

# Create Listing View
@login_required
# def create_listing(request: HttpRequest, autofill_data: Listing | None = None) -> HttpResponse:
#     if not autofill_data and request.method == "POST":
#         form = ListingForm(request.POST, request.FILES, instance=Listing(seller=request.user))    
#         files=request.FILES.getlist('images')
#         if form.is_valid():
#             form.save()
#             return redirect("dashboard:dashboard") 
#         else:
#             print(form.errors)

#     else:
#         form = ListingForm(instance=autofill_data)
#     return render(request, "create_listing.html", {"form": form})
def create_listing(request, autofill_data: Listing | None = None) -> HttpResponse:
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            images = request.FILES.getlist('images')
            for image in images:
                ListingImage.objects.create(listing=listing, image=image)
            return redirect("dashboard:dashboard")
        else:
            print(form.errors)
    else:
        form = ListingForm(instance=autofill_data)
        image_form = ListingImage()
    return render(request, "create_listing.html", {"form": form})

# Listing Page with Filtering
def browse_search(request):
    # Adding an item to the cart via POST
    if request.method == "POST":
        listing_id = request.POST.get("listing_id")
        if listing_id:
            listing_id = int(listing_id)
            cart = request.session.get("cart", [])
            if listing_id not in cart:
                cart.append(listing_id)
                request.session["cart"] = cart
                messages.success(request, "Item added to cart!")
        return redirect("listings:browse_search")
    
    # For GET requests, simply display listings with selected filters:
    listings = Listing.objects.filter(sold=False) # Filter to only unsold listings.

    search = SearchForm(request.GET)
    if search.is_valid():
         # I stripped out the dash for matching ISBN, but maybe we should regex check that it is an ISBN first.
         # If we know it's an ISBN we can also simply the query filter to only match ISBN.
        query = search.cleaned_data["q"].replace("-", "")
        location_filter = search.cleaned_data["location"]

        # Filter listings based on search query
        if query:
            listings = listings.filter(
                Q(title__icontains=query) | Q(author__icontains=query) | Q(isbn__exact=query)
            )  # Filter by title, author, and ISBN containing the search term

        # Apply location filter
        if location_filter == "Global":
            listings = listings.filter(location="Global")
        elif location_filter == "Local":
            listings = listings.filter(location="Local")

    # Order results by newest first
    listings = listings.order_by("-id").distinct()

    return render(request, "browse.html", {
        "listings": listings,
        "search_form": search
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
                messages.success(request, "Item added to cart!") 
        return redirect("cart:cart")

    return render(request, "textbook_details.html", {"listing": listing})

@login_required
def edit_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id, seller=request.user)

    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect("dashboard:dashboard")
    else:
        form = ListingForm(instance=listing)

        for field in form.fields:
            if field not in ["price", "additional_details", "coursecode"]:
                form.fields[field].widget.attrs['readonly'] = True
                
    return render(request, "edit_listing.html", {"form": form})

@login_required
def delete_listing(request: HttpRequest, listing_id) -> HttpResponse:
    try:
        listing = Listing.objects.get(pk=listing_id, seller=request.user)
        listing.delete()
    finally:
        return redirect("dashboard:dashboard")

