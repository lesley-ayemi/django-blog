# from blog.views import profile
# import django
from django.db.models.signals import post_save
from django.contrib.auth.models import Group, User
from .models import Account, Profile

def create_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance
        )
post_save.connect(create_user, sender=Account)