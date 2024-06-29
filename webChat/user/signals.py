from .models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete

def createProfile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(
            user = instance,
            username = instance.username,
        )

def deleteProfile(sender, instance, **kwargs):
    try:
        instance.user.delete()
    except:
        pass
   

post_save.connect(createProfile, sender=User)
post_delete.connect(deleteProfile, sender=Profile)
