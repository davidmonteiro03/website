# import Django modules
from django.db import models # Django database
from django.utils.crypto import get_random_string # Generate random string

# Model to store API links
class ApiLink(models.Model):
	id = models.AutoField(primary_key=True) # primary key
	link = models.CharField(max_length=255) # character field with a maximum length of 255 characters
	name = models.CharField(max_length=255) # character field with a maximum length of 255 characters
	token = models.CharField(max_length=64, unique=True, editable=False, default=get_random_string(64)) # character field with a maximum length of 64 characters, unique, not editable, and default value is a random string of 64 characters
