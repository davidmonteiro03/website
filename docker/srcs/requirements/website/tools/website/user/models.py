# import Python modules
import os

# import Django modules
from django.db import models # Django models
from django.core.files.storage import default_storage # Default storage

# Function to get user directory path
def user_directory_path(instance, filename):
	extension = filename.split('.')[-1] # Get file extension
	new_filename = f"{instance.username}.{extension}" # New filename
	return os.path.join('profilephotos', new_filename) # Return new filename

# Model to store user data
class User(models.Model):
	id = models.AutoField(primary_key=True) # primary key
	fname = models.CharField(max_length=255) # character field with a maximum length of 255 characters
	lname = models.CharField(max_length=255) # character field with a maximum length of 255 characters
	username = models.CharField(max_length=255) # character field with a maximum length of 255 characters
	password = models.CharField(max_length=255) # character field with a maximum length of 255 characters
	email = models.CharField(max_length=255) # character field with a maximum length of 255 characters
	profilephoto = models.ImageField(upload_to=user_directory_path) # image field with a file path
	def save(self, *args, **kwargs): # Save method
		if self.pk is not None: # Check if primary key exists
			orig = User.objects.get(pk=self.pk) # Get original user
			if orig.username != self.username: # Check if username is different
				old_file_path = self.profilephoto.path # Get old file path
				new_filename = f"{self.username}.{self.profilephoto.name.split('.')[-1]}" # New filename
				new_file_path = os.path.join(os.path.dirname(old_file_path), new_filename) # New file path
				if default_storage.exists(old_file_path): # Check if old file path exists
					if default_storage.exists(new_file_path): # Check if new file path exists
						default_storage.delete(new_file_path) # Delete new file path
					default_storage.save(new_file_path, default_storage.open(old_file_path)) # Save new file path
					default_storage.delete(old_file_path) # Delete old file path
				self.profilephoto.name = os.path.join('profilephotos', new_filename) # Set new profile photo name
		super().save(*args, **kwargs) # Save user data

# Model to store session data
class Session(models.Model):
	id = models.AutoField(primary_key=True) # primary key
	user = models.ForeignKey(User, on_delete=models.CASCADE) # foreign key to User model (if user is deleted, session is deleted)
	session_token = models.CharField(max_length=255) # character field with a maximum length of 255 characters
