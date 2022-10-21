from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver


from .models import Profile, Post


@receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
def create_profile(sender,instance,created, **kwargs):
    user = instance
    if created:
        profile = Profile(user=user)
        profile.save()

@receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
def create_post(sender,instance,created, **kwargs):
    user = instance
    if created:
        post = Post(user=user)
        post.save()

