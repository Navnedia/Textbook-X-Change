from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from listings.models import Listing
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
# Create views related to the cart and checkout functionality:

def cart_view(request):
    # Handle removal of an item from the cart
    if request.method == "POST":
        remove_id = request.POST.get("remove_listing_id")
        if remove_id:
            remove_id = int(remove_id)
            cart = request.session.get("cart", [])
            if remove_id in cart:
                cart.remove(remove_id)
                request.session["cart"] = cart
        return redirect("cart:cart")
    # For GET requests, display the cart items
    cart_item_ids = request.session.get("cart", [])
    cart_items = Listing.objects.filter(id__in=cart_item_ids)
    return render(request, "cart/cart.html", {"cart_items": cart_items})

@login_required
def checkout_view(request, listing_id):
    # Retrieve the current cart from the session
    cart = request.session.get("cart", [])
    if listing_id not in cart:
        return redirect("cart:cart")
    # Get the listing object
    listing = get_object_or_404(Listing, id=listing_id)
    if request.method == "POST":
        # Retrieve shipping and payment details from POST data
        # No need to actually retrieve this info as of demo 1
        #shipping_address = request.POST.get("shipping_address")
        #city = request.POST.get("city")
        #state = request.POST.get("state")
        #zip_code = request.POST.get("zip_code")
        #cc_number = request.POST.get("cc_number")
        #cc_expiration = request.POST.get("cc_expiration")
        #cc_cvv = request.POST.get("cc_cvv")
        # Remove the listing from the session cart
        listing.sold = True
        listing.save()

        # Send email to the seller (listing's creator)
        send_listing_sold_email(listing.seller, listing)
        
        cart.remove(listing_id)
        request.session["cart"] = cart
        # Add a success message 
        messages.success(request, "Item purchased successfully!")
        # Redirect to a confirmation page or back to the cart
        return redirect("cart:cart")
    return render(request, "cart/checkout.html", {"listing": listing})
# Function to send email on listing sale
def send_listing_sold_email(user, listing):
    subject = "Your Textbook Listing Has Been Sold!"
    message = render_to_string('cart/listing_sold_email.html', {
        'user': user,
        'listing': listing,
    })
    # Send the email with the HTML content
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        html_message=message  # This ensures the email is sent as HTML
    )


# In your checkout view or after the sale is confirmed
def checkout(request, item_id):
    listing = get_object_or_404(Listing, id=item_id)
    user = request.user
    # Handle the purchase logic here
    send_listing_sold_email(user, listing)