from django.conf import settings
from django.urls import reverse
from django.db import models
from core.models import School, Book
from login.models import Profile

# Create Listing related models here:

class Listing(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    # courses = models.ManyToManyField(Course, blank=True, related_name="listings")
    book = models.ForeignKey(Book, null=True, on_delete=models.PROTECT, related_name="Listings", db_index=True)

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

    location = models.CharField(max_length=64, choices=Location, default=Location.LOCAL) #! this somehow needs to be a reference to the users university so that we can sort by the university for local/global.
    
    #! At least one of these must be selected. 
    allows_local_pickup = models.BooleanField(default=False)
    allows_shipping = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # coursecode=models.CharField(max_length=64, null=True, blank=True)

    @property
    def title(self):
        return self.book.title
    
    @property
    def isbn(self):
        return self.book.isbn
    
    @property
    def author(self):
        return self.book.authors.first()
    
    @property
    def authors(self):
        return self.book.authors.all()
    
    @property
    def coursecode(self):
        first_course = self.book.courses.first()
        return first_course.code if first_course else None
    
    @property
    def courses(self):
        return self.book.courses.all()

    # @property # Is this technically a property, I don't think so...
    def local_school(self) -> School | None:
        seller_profile = Profile.objects.filter(user=self.seller).first()
        return seller_profile.school if seller_profile else None

    def get_absolute_url(self):
        return reverse('listings:textbook_details', kwargs={'pk': self.pk})

    def __str__(self):  
        return f"{self.title} for {self.price}"
    

class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="listing_images/")

    def __str__(self):
        return f"Image for {self.listing.title}"
