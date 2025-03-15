from django.db import models
from listings.models import Listing
from django.conf import settings

# Create your models here.
class Order(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True, db_index=True)
    shipping_address = models.CharField(max_length=255, blank=True, null=True)
    has_shipped = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk} for {self.listing.title}"
