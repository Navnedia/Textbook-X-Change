from listings.models import Listing
from django.http import HttpRequest

def notifications(request: HttpRequest):
    if request.user.is_authenticated:
        # Check if the current user has any sold items.
        sold = Listing.objects.filter(seller=request.user, sold=True).exists()
        return { "dashboard_notification": sold }
    
    return {}
