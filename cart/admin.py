from django.contrib import admin
from .models import Order

# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('listing', 'buyer', 'shipping_address', 'has_shipped', 'created_at')
    search_fields = ('listing__book__title', 'listing__book__isbn', 'buyer__username', 'buyer__profile__school__name', 'shipping_address')
    list_filter = ('has_shipped', 'created_at')