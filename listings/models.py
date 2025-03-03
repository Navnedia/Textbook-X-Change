from django.db import models
from django.db.models import Index
from django.db.models.functions import Lower
from django.contrib.auth.models import User
from login.models import Profile
from core.models import School
from django.urls import reverse

# Create Listing related models here:


class Course(models.Model):
    code = models.CharField(max_length=50)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='courses')

    class Meta:
        constraints = [ 
            # Define a constraint on the DB that the course code and school must be a unique combo
            # so a course can't be defined multiple times.
            models.UniqueConstraint( 
                name="unique_course_at_school", 
                fields=["code", "school"]
            )
        ]

    def __str__(self):
        return self.code
    

class Author(models.Model):
    name = models.CharField(max_length=70)

    class Meta:
        indexes = [
            Index(Lower("name"), name="lower_name_idx")
        ]

    def __str__(self):
        return self.name

    
class Book(models.Model):
    isbn = models.CharField(max_length=13, unique=True) #! We must sanitize and remove dash.
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, null=True, blank=True, related_name="Books")
    summary = models.CharField(max_length=2000, null=True, blank=True) # The official book description if available.
    courses = models.ManyToManyField(Course, null=True, blank=True, related_name="Books")
    # Stock_cover = models.ImageField(upload_to="listing_images/", blank=True, null=True) # The official stock cover image.
    # edition?
    # subject/category tags?
    # created_by? (system, user, autofilled) or just created_manually flag.

    class Meta:
        indexes = [
            Index(Lower("title"), name="lower_title_idx")
        ]

    def __str__(self):
        return self.title



class Listing(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    courses = models.ManyToManyField(Course, null=True, blank=True, related_name="listings")
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name="Listings", db_index=True)

    is_active = models.BooleanField(default=True) # is_active (some sort of way to track the state so we know when to show it or not).


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
    
    #! At least one of these must be selected. 
    allows_local_pickup = models.BooleanField(default=False)
    allows_shipping = models.BooleanField(default=False)

    # coursecode=models.CharField(max_length=64, null=True, blank=True)

    # @property # Is this technically a property, I don't think so...
    def local_school(self) -> School | None:
        seller_profile = Profile.objects.filter(user=self.seller).first()
        return seller_profile.school if seller_profile else None

    def get_absolute_url(self):
        return reverse("textbook_details", kwargs={"pk": self.pk})

    def __str__(self):  
        return f"{self.title} for {self.price}"
