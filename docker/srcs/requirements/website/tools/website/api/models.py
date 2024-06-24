# import Django modules
from django.db import models # Django database

# Model to store API links
class ApiLink(models.Model):
	id = models.AutoField(primary_key=True) # primary key
	link = models.CharField(max_length=255) # character field with a maximum length of 255 characters
	name = models.CharField(max_length=255) # character field with a maximum length of 255 characters
