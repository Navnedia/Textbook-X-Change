from django.conf import settings
from django.db import models
from core.models import School

# Define user/account/auth related models:

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="profile"
    )
    
    school = models.ForeignKey(School, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="students"
    )
