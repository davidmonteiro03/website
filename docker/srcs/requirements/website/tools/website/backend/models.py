from django.db import models

# Create your models here.
class Users(models.Model):
	id = models.AutoField(primary_key=True)
	fname = models.CharField(max_length=255)
	lname = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	token = models.CharField(max_length=255)
