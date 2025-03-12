from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from cart.models import Order
from listings.models import Listing
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
# Create views related to the cart and checkout functionality:

@login_required
def cart_view(request):
    """View the cart and past orders."""
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

    cart_item_ids = request.session.get("cart", [])
    cart_items = Listing.objects.filter(id__in=cart_item_ids)

    # Fetch order history for the logged-in user
    orders = Order.objects.filter(buyer=request.user).order_by("-id")

    return render(
        request, "cart/cart.html", {"cart_items": cart_items, "orders": orders}
    )


@login_required
def checkout_view(request, listing_id):
    cart = request.session.get("cart", [])
    if listing_id not in cart:
        return redirect("cart:cart")

    listing = get_object_or_404(Listing, id=listing_id)

    if request.method == "POST":
        shipping_address = request.POST.get("shipping_address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zip_code = request.POST.get("zip_code")

        # Combine shipping fields into a single address
        full_address = f"{shipping_address}, {city}, {state} {zip_code}"

        # Create the Order
        order = Order.objects.create(
            buyer=request.user,
            listing=listing,
            shipping_address=full_address
        )

        # Mark listing as sold
        listing.sold = True
        listing.save()

        # Send email to the seller (listing's creator)
        send_listing_sold_email(listing.seller, listing)

        cart.remove(listing_id)
        request.session["cart"] = cart

        messages.success(request, "Item purchased successfully!")
        return redirect("cart:order_confirmation", order_id=order.pk)
    return render(request, "cart/checkout.html", {"listing": listing})


@login_required
def order_confirmation_view(request, order_id):
    # Make sure the user is the buyer, so nobody else can peek
    order = get_object_or_404(Order, pk=order_id, buyer=request.user)
    return render(request, "cart/order_confirmation.html", {"order": order})


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
        html_message=message,  # This ensures the email is sent as HTML
        fail_silently=True
    )
