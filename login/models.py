from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
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

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()