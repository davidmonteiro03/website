# import Python modules
import os # Miscellaneous operating system interfaces

# import Django modules
from django.conf import settings # Django settings

# import API
from api import api # API

# Function to get templates
# :param app: application name
# :return: list of templates
def get_templates(app: str) -> list[str]:
	dir_path = os.path.join(settings.BASE_DIR, app, 'templates') # Get directory path
	files = os.listdir(dir_path) # Get list of files
	for i in range(0, len(files), 1): # Iterate over files
		files[i] = files[i].split('.')[0] # Remove extension
	for key in api.__dict__: # Iterate over API
		if callable(api.__dict__[key]) and not key in files: # Check if key is callable and not in files
			files.append(key) # Append key to files
	return files # Return list of templates
