from django.conf import settings
from django.db import models
from core.models import School #, Course, Author, Book
from django.urls import reverse

# Create Listing related models here:

# class Listing(models.Model):
#     seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
#     courses = models.ManyToManyField(Course, null=True, blank=True, related_name="listings")
#     book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name="Listings", db_index=True)

#     is_active = models.BooleanField(default=True) # is_active (some sort of way to track the state so we know when to show it or not).


#     additional_details = models.TextField(null=True, blank=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     image = models.ImageField(upload_to="listing_images/", blank=True, null=True)

#     class Condition(models.TextChoices):
#         NEW = "N", "New"
#         LIKE_NEW = "LN", "Like New"
#         GOOD = "G", "Good"
#         ACCEPTABLE = "A", "Acceptable"

#     condition = models.CharField(max_length=3, choices=Condition, default=Condition.NEW)

#     class Location(models.TextChoices):
#         LOCAL = "L", "Local"
#         GLOBAL = "G", "Global"

#     location = models.CharField(max_length=64, choices=Location, default=Location.LOCAL) #! this somehow needs to be a reference to the users university so that we can sort by the university for local/global.
    
#     #! At least one of these must be selected. 
#     allows_local_pickup = models.BooleanField(default=False)
#     allows_shipping = models.BooleanField(default=False)

#     # coursecode=models.CharField(max_length=64, null=True, blank=True)

#     # @property # Is this technically a property, I don't think so...
#     def local_school(self) -> School | None:
#         seller_profile = Profile.objects.filter(user=self.seller).first()
#         return seller_profile.school if seller_profile else None

#     def get_absolute_url(self):
#         return reverse("textbook_details", kwargs={"pk": self.pk})

#     def __str__(self):  
#         return f"{self.title} for {self.price}"


class Listing(models.Model):
    seller=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    title=models.CharField(max_length=64, null=True, blank=True)
    isbn=models.CharField(max_length=64)
    author=models.CharField(max_length=64, null=True, blank=True)

    additional_details=models.TextField(null=True, blank=True) #! listing additional details?
    price=models.DecimalField(max_digits=10, decimal_places=2)
    sold=models.BooleanField(default=False)
    class Condition(models.TextChoices):
        NEW = "New", "New"
        LIKE_NEW = "Like New", "Like New"
        GOOD = "Good", "Good"
        ACCEPTABLE = "Acceptable", "Acceptable"

    condition = models.CharField(max_length=20, choices=Condition, default=Condition.NEW)

    class Location(models.TextChoices):
        LOCAL = "Local", "Local"
        GLOBAL = "Global", "Global"

    location=models.CharField(max_length=64, choices=Location, default=Location.LOCAL) #! this somehow needs to be a reference to the users university so that we can sort by the university for local/global.
    coursecode=models.CharField(max_length=64, null=True, blank=True)
    
    def get_absolute_url(self):
        return reverse("textbook_details", kwargs={"pk": self.pk})

    def __str__(self):  
        return f"{self.title} by {self.author} for {self.price}"
    
class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="listing_images/")

    def __str__(self):
        return f"Image for {self.listing.title}"
