from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse
from cart.models import Order
from listings.models import Listing
from django.contrib.auth.decorators import login_required
# Define dashboard related views here:

@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    listings = Listing.objects.filter(seller=request.user).order_by("-id")
    orders = Order.objects.filter(listing__seller=request.user).order_by("-id")
    
    return render(request, "dashboard/dashboard.html", {"listings": listings, "orders": orders})

@login_required
def confirm_shipment(request, order_id):
    """Mark an order as shipped."""
    order = get_object_or_404(Order, id=order_id, listing__seller=request.user)

    if order and order.shipping_info:  
        order.has_shipped = True
        order.save()
        return JsonResponse({"message": "Shipment confirmed!"})
    
    return JsonResponse({"error": "Cannot confirm shipment without buyer shipping details."}, status=400)