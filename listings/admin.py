from django.contrib import admin
from .models import Listing, ListingImage
from core.models import Book
from cart.models import Order

class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 0
    fields = ('image',)


class OrderInline(admin.StackedInline):
    model = Order
    extra = 0
    max_num = 1
    readonly_fields = ('created_at',)


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('book__title', 'book__isbn', 'price', 'condition', 'location', 'seller__username', 'sold')
    search_fields = ('seller__username', 'book__title', 'book__isbn', 'book__authors__name', 'book__courses__code', 'seller__profile__school__name')
    list_filter = ('condition', 'location', 'sold', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ListingImageInline, OrderInline]


@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ('listing', 'image')
