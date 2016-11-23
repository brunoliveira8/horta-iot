from django.db import models
from registration.signals import user_registered
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Dados(models.Model):
    umidade_solo = models.DecimalField(max_digits=5, decimal_places=2)
    umidade_ar = models.DecimalField(max_digits=5, decimal_places=2)
    temperatura = models.DecimalField(max_digits=5, decimal_places=2)
    criado_em = models.DateTimeField(default=datetime.now)

class Atuador(models.Model):
    status = models.BooleanField(default=False)
    criado_em = models.DateTimeField(default=datetime.now)


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    is_human = models.BooleanField(default=True)

    def __unicode__(self):
        return self.user


def user_registered_callback(sender, user, request, **kwargs):
    profile = UserProfile(user=user)
    profile.is_human = bool(request.POST["is_human"])
    profile.save()


user_registered.connect(user_registered_callback)
