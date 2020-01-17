from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Client(AbstractUser):
    telephone = models.CharField(max_length=30, null=True, unique=True)
    originate = models.CharField(max_length=30, null=True)
    is_pay = models.BooleanField(default=False)
    register_time = models.DateTimeField(auto_now_add=True)
    login_num = models.IntegerField(default=0)

    class Meta:
        db_table = 'client'

    def __str__(self):
        return self.username
