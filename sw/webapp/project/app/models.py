from django.db import models
from registration.signals import user_registered
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    is_human = models.BooleanField(default=True)
 
    def __unicode__(self):
        return self.user


def user_registered_callback(sender, user, request, **kwargs):
    profile = UserProfile(user = user)
    profile.is_human = bool(request.POST["is_human"])
    profile.save()
 
user_registered.connect(user_registered_callback)