from django.db import models

# Create your models here.
class ApiLink(models.Model):
	id = models.AutoField(primary_key=True)
	link = models.CharField(max_length=255)
	name = models.CharField(max_length=255)
