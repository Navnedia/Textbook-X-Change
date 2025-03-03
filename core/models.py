from django.db import models

# Create your models here.

class School(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # Additional data: website domain, geo data (lat/long, state, city, zip).

    def __str__(self):
        return self.name