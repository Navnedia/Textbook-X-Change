from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create Listing related models here:

class Listing(models.Model):
    seller=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title=models.CharField(max_length=64, null=True, blank=True)
    isbn=models.CharField(max_length=64)
    author=models.CharField(max_length=64, null=True, blank=True)

    additional_details=models.TextField(null=True, blank=True) #! listing additional details?
    price=models.DecimalField(max_digits=10, decimal_places=2)
    image=models.ImageField(upload_to="listing_images/", blank=True, null=True)

    class Condition(models.TextChoices):
        NEW = "N", "New"
        LIKE_NEW = "LN", "Like New"
        GOOD = "G", "Good"
        ACCEPTABLE = "A", "Acceptable"

    condition = models.CharField(max_length=3, choices=Condition, default=Condition.NEW)

    class Location(models.TextChoices):
        LOCAL = "L", "Local"
        GLOBAL = "G", "Global"

    location=models.CharField(max_length=64, choices=Location, default=Location.LOCAL) #! this somehow needs to be a reference to the users university so that we can sort by the university for local/global.
    coursecode=models.CharField(max_length=64, null=True, blank=True)
    
    def get_absolute_url(self):
        return reverse("textbook_details", kwargs={"pk": self.pk})

    def __str__(self):  
        return f"{self.title} by {self.author} for {self.price}"
