from django.contrib import admin
from .models import Listing, ListingImage
from cart.models import Order

class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 0
    fields = ('image',)

class OrderInline(admin.StackedInline):
    model = Order
    extra = 0
    fields = ('buyer', 'shipping_address', 'has_shipped', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'price', 'condition', 'location', 'sold',)
    search_fields = ('title', 'isbn', 'author', 'coursecode')
    list_filter = ('condition', 'location', 'sold')
    inlines = [ListingImageInline, OrderInline]

@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ('listing', 'image')
