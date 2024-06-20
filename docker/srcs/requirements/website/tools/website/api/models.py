# import Python modules
import secrets

# import Django modules
from django.db import models # Django models

# ApiLink model
class ApiLink(models.Model):
	id = models.AutoField(primary_key=True) # primary key
	link = models.CharField(max_length=255, unique=True) # character field with a maximum length of 255 characters
	name = models.CharField(max_length=255) # character field with a maximum length of 255 characters
	token = models.CharField(max_length=64, blank=True, editable=False, unique=True) # character field with a maximum length of 64 characters and a default value of a 64-character token

	def save(self, *args, **kwargs):
		if not self.token:
			self.token = secrets.token_hex(64)
		super().save(*args, **kwargs)
