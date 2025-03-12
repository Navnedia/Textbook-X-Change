from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from cart.models import Order
from listings.models import Listing
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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

        cart.remove(listing_id))
        request.session["cart"] = cart

        messages.success(request, "Item purchased successfully!")
        return redirect("cart:order_confirmation", order_id=order.pk)
    return render(request, "cart/checkout.html", {"listing": listing})

@login_required
def order_confirmation_view(request, order_id):
    # Make sure the user is the buyer, so nobody else can peek
    order = get_object_or_404(Order, pk=order_id, buyer=request.user)
    return render(request, "cart/order_confirmation.html", {"order": order})
