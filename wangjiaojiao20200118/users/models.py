from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


class AuthUser(AbstractUser):

    mobilephone = models.CharField('Mobilephone', max_length=50, blank=True)
    customersource = models.CharField('CustomerSource', max_length=50, blank=True)
    is_pay = models.CharField('is not pay', max_length=50, blank=True)
    loginnum = models.IntegerField('LoginNumber', blank=True)

    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return self.username




