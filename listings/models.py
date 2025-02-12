from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Listing(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title=models.CharField(max_length=64, null=True, blank=True)
    isbn=models.CharField(max_length=64)
    author=models.CharField(max_length=64, null=True, blank=True)
    description=models.TextField(null=True, blank=True)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    image=models.ImageField(upload_to="listing_images/", blank=True, null=True)
    CONDITION_CHOICES = [
    ('New', 'New'),
    ('Like New', 'Like New'),
    ('Good', 'Good'),
    ('Acceptable', 'Acceptable'),
]
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    LOCATION_CHOICES = [
    ('Global', 'Global'),
    ('Local', 'Local'),
    ]
    location=models.CharField(max_length=64, choices=LOCATION_CHOICES)
    coursecode=models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):  
        return f"{self.title} by {self.author} for {self.price}"
