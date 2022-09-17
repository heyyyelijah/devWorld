from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


# instance = name of user that was created/updated/deleted
# @receiver(post_save, sender=Profile)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email=user.email,
            name=user.first_name, 
        )


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    # if condition is to make sure that the profile has not just been created 
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save() 


# 
# @receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass


# TRIGGERED AFTER A USER IS CREATED
post_save.connect(createProfile, sender=User)
# TRIGGERED AFTER A PROFILE IS UPDATED
post_save.connect(updateUser, sender=Profile)
# # TRIGGERED IF PROFILE IS DELETED
post_delete.connect(deleteUser, sender=Profile)