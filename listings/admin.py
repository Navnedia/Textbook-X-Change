from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Listing, Course, Book, Author

# Register your models here.
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Course)
admin.site.register(Listing)