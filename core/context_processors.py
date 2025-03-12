from cart.models import Order
from listings.models import Listing
from django.db.models import Q
from django.http import HttpRequest

def notifications(request: HttpRequest):
    if request.user.is_authenticated:
        # If the user is a seller with an item that needs to be shipped, or a buyer when the item has shipped.
        shipping_status = Order.objects.filter(
            Q(listing__seller=request.user, has_shipped=False) |
            Q(buyer=request.user, has_shipped=True)
        ).exists()
        return { "dashboard_notification": shipping_status }
    
    return {}
