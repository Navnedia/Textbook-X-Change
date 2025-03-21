from django.conf import settings
from django.db import models
from django.urls import reverse


class Listing(models.Model):
    seller=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    title=models.CharField(max_length=64, null=True, blank=True)
    isbn=models.CharField(max_length=64)
    author=models.CharField(max_length=64, null=True, blank=True)
    additional_details=models.TextField(null=True, blank=True) #! listing additional details?
    coursecode=models.CharField(max_length=64, null=True, blank=True)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    sold=models.BooleanField(default=False)

    class Condition(models.TextChoices):
        NEW = "New", "New"
        LIKE_NEW = "Like New", "Like New"
        GOOD = "Good", "Good"
        ACCEPTABLE = "Acceptable", "Acceptable"

    class Location(models.TextChoices):
        LOCAL = "Local", "Local"
        GLOBAL = "Global", "Global"

    condition = models.CharField(max_length=20, choices=Condition, default=Condition.NEW)
    location=models.CharField(max_length=64, choices=Location, default=Location.LOCAL) #! this somehow needs to be a reference to the users university so that we can sort by the university for local/global.
    

    def get_absolute_url(self):
        return reverse('listings:textbook_details', kwargs={'pk': self.pk})

    def __str__(self):  
        return f"{self.title} by {self.author} for {self.price}"
    
class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="listing_images/")

    def __str__(self):
        return f"Image for {self.listing.title}"
