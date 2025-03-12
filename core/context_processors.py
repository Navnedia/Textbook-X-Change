from cart.models import Order
from django.db.models import Q
from django.http import HttpRequest

def notifications(request: HttpRequest):
    if request.user.is_authenticated:
        # If the user is a seller with an item that needs to be shipped, or a buyer when the item has shipped.
        seller_ship_order = Order.objects.filter(
            Q(listing__seller=request.user, has_shipped=False)
        ).exists()
        buyer_order_shipped = Order.objects.filter(
            Q(buyer=request.user, has_shipped=True)
        ).exists()
        return { 
            "dashboard_notification": seller_ship_order,
            "cart_notification": buyer_order_shipped
        }
    
    return {}
