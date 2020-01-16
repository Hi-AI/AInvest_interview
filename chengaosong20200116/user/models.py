from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel
# Create your models here.                                                  


class User(AbstractUser, BaseModel):
	name=models.CharField(max_length=10,null=True)
	phonenumber=models.CharField(max_length=20,unique=True,null=True)
	more_informations=models.CharField(max_length=50)
	agent=models.CharField(max_length=50)
	is_pay=models.BooleanField(default=False)
	login_times=models.IntegerField(default=0)

	class Meta:
		db_table = 'user'
		verbose_name = 'my_user'
		verbose_name_plural = verbose_name
	def __str__(self):
		return self.username