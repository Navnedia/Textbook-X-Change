from django.db import models
from django.db.models import Index
from django.db.models.functions import Lower

# Define core data models that are fundamental and domain-specific.
# These models are likely to be used accross many different app modules.

class School(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # Additional data: website domain, geo data (lat/long, state, city, zip).

    def __str__(self):
        return self.name
    

# class Course(models.Model):
#     code = models.CharField(max_length=50)
#     school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='courses')

#     class Meta:
#         constraints = [ 
#             # Define a constraint on the DB that the course code and school must be a unique combo
#             # so a course can't be defined multiple times.
#             models.UniqueConstraint( 
#                 name="unique_course_at_school", 
#                 fields=["code", "school"]
#             )
#         ]

#     def __str__(self):
#         return self.code
    

# class Author(models.Model):
#     name = models.CharField(max_length=70)

#     class Meta:
#         indexes = [
#             Index(Lower("name"), name="lower_name_idx")
#         ]

#     def __str__(self):
#         return self.name

    
# class Book(models.Model):
#     isbn = models.CharField(max_length=13, unique=True) #! We must sanitize and remove dash.
#     title = models.CharField(max_length=255)
#     authors = models.ManyToManyField(Author, null=True, blank=True, related_name="Books")
#     summary = models.CharField(max_length=2000, null=True, blank=True) # The official book description if available.
#     courses = models.ManyToManyField(Course, null=True, blank=True, related_name="Books")
#     # Stock_cover = models.ImageField(upload_to="listing_images/", blank=True, null=True) # The official stock cover image.
#     # edition?
#     # subject/category tags?
#     # created_by? (system, user, autofilled) or just created_manually flag.

#     class Meta:
#         indexes = [
#             Index(Lower("title"), name="lower_title_idx")
#         ]

#     def __str__(self):
#         return self.title