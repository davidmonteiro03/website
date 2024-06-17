from django.db import models
from django.core.files.storage import default_storage
import os

def user_directory_path(instance, filename):
	extension = filename.split('.')[-1]
	new_filename = f"{instance.username}.{extension}"
	return os.path.join('profilephotos', new_filename)

# Create your models here.
class User(models.Model):
	id = models.AutoField(primary_key=True)
	fname = models.CharField(max_length=255)
	lname = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	profilephoto = models.ImageField(upload_to=user_directory_path)
	def save(self, *args, **kwargs):
		if self.pk is not None:
			orig = User.objects.get(pk=self.pk)
			if orig.username != self.username:
				old_file_path = self.profilephoto.path
				new_filename = f"{self.username}.{self.profilephoto.name.split('.')[-1]}"
				new_file_path = os.path.join(os.path.dirname(old_file_path), new_filename)
				if default_storage.exists(old_file_path):
					if default_storage.exists(new_file_path):
						default_storage.delete(new_file_path)
					default_storage.save(new_file_path, default_storage.open(old_file_path))
					default_storage.delete(old_file_path)
				self.profilephoto.name = os.path.join('profilephotos', new_filename)
		super().save(*args, **kwargs)

class Session(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	session_token = models.CharField(max_length=255)
