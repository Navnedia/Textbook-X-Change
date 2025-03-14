from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse
from .forms import ListingForm, PrelistForm, SearchForm, FileFieldForm, MultipleFileField, MultipleFileInput
from .models import Listing, ListingImage
from django.db.models import Q
from .services.autofill import PrelistSuggestionsProvider
from django.contrib.auth.decorators import login_required
from wishlist.models import WishList
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
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
def create_listing(request: HttpRequest, autofill_data: Listing | None = None) -> HttpResponse:
    if not autofill_data and request.method == "POST":
        form = ListingForm(request.POST, request.FILES, instance=Listing(seller=request.user))
        if form.is_valid():
            listing = form.save()  # Save the listing and assign it to the 'listing' variable

            images = request.FILES.getlist('images')
            for image in images:
                ListingImage.objects.create(listing=listing, image=image)

            # Now check for any requests that match the ISBN of the new listing
            matching_requests = WishList.objects.filter(isbn=listing.isbn)  # Find matching requests

            # Send email for each matching request
            for req in matching_requests:
                subject = "Your Requested Textbook is Now Available!"
                message = render_to_string('wishlist/request_match_email.html', {
                    'user': req.user,
                    'listing': listing,  # The listing variable is now available here
                    'listing_url': request.build_absolute_uri(listing.get_absolute_url()),  # Assuming this method exists
                })
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [req.user.email],
                    html_message=message,  # Sends the email as HTML
                    fail_silently=True
                )

            # Redirect to the dashboard after the listing is created and email is sent
            return redirect("dashboard:dashboard")
    else:
        form = ListingForm(instance=autofill_data)
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

    # For GET requests, display listings with selected filters:
    listings = Listing.objects.filter(sold=False)  # Filter to only unsold listings.

    search = SearchForm(request.GET)
    if search.is_valid():
        query = search.cleaned_data["q"].replace("-", "")
        location_filter = search.cleaned_data["location"]

        # Filter listings based on search query
        if query:
            listings = listings.filter(
                Q(title__icontains=query) | Q(author__icontains=query) | Q(isbn__exact=query)
            )

        # Apply location filter
        if location_filter == "Global":
            listings = listings.filter(location="Global")
        elif location_filter == "Local":
            listings = listings.filter(location="Local")

    # Apply price range filter if min_price or max_price is provided
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        listings = listings.filter(price__gte=min_price)

    if max_price:
        listings = listings.filter(price__lte=max_price)

    # Sorting logic (from previous update)
    sort_by = request.GET.get('sort_by', '')
    if sort_by == 'price_low_high':
        listings = listings.order_by('price')
    elif sort_by == 'price_high_low':
        listings = listings.order_by('-price')
    elif sort_by == 'best_sellers':
        listings = listings.order_by('-sales_count')  # Assuming `sales_count` is a field
    elif sort_by == 'newly_listed':
        listings = listings.order_by('-created_at')  # Assuming `created_at` is a datetime field
    elif sort_by == 'most_viewed':
        listings = listings.order_by('-view_count')  # Assuming `view_count` is a field

    # Order results by newest first if no sorting is applied
    if not sort_by:
        listings = listings.order_by("-id")

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

