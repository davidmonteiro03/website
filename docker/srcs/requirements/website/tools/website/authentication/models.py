from django.db import models

# Create your models here.
class Users(models.Model):
	id = models.AutoField(primary_key=True)
	fname = models.CharField(max_length=100)
	lname = models.CharField(max_length=100)
	username = models.CharField(max_length=100)
	email = models.EmailField()
	password = models.CharField(max_length=100)
