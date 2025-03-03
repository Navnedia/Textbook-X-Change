from django.db import models
from django.contrib.auth.models import User
from core.models import School

# Define user/account/auth related models:

class Profile(models.Model):
    user = models.OneToOneField(User, 
        on_delete=models.CASCADE, 
        related_name="profile"
    )
    
    school = models.ForeignKey(School, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="students"
    )
