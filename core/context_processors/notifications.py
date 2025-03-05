from listings.models import Listing
from django.http import HttpRequest, HttpResponse

def sold(request: HttpRequest):
    if request.user.is_authenticated:
        sold = Listing.objects.filter(seller=request.user, sold=True).exists()
        return { "has_sold": sold }
    return {}
