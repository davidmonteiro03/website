# import Django modules
from django.db import models # Django database
from django.utils.crypto import get_random_string # Generate random string

# import API
from . import api # import API

# Model to store API links
class ApiLink(models.Model):
	id = models.AutoField(primary_key=True) # primary key
	link = models.CharField(max_length=255, unique=True) # character field with a maximum length of 255 characters and unique
	name = models.CharField(max_length=255, editable=False) # character field with a maximum length of 255 characters and not editable
	token = models.CharField(max_length=64, unique=True, editable=False) # character field with a maximum length of 64 characters, unique, not editable, and default value is a random string of 64 characters
	def save(self, *args, **kwargs):
		if not self.name:
			try:
				self.name = api.__dict__[self.link]()['name']
			except:
				self.name = self.link
		if not self.token:
			self.token = get_random_string(length=64)
		super().save(*args, **kwargs)
