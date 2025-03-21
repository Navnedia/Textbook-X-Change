from django.db import models

# Define core data models that are fundamental and domain-specific.
# These models are likely to be used accross many different app modules.

class School(models.Model):
    name = models.CharField(max_length=100, unique=True)

    # This might be relevant later if we wanted to autoselect a school based on account email domain.
    website = models.URLField(null=True, blank=True)

    # These location details would be relevant later if we choose to do more fine grain radius location searching, etc.
    long = models.DecimalField(max_digits=22, decimal_places=16, null=True, blank=True)
    lat = models.DecimalField(max_digits=22, decimal_places=16, null=True, blank=True)

    def __str__(self):
        return self.name
