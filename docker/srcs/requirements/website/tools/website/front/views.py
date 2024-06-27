# import Python modules
import json # JSON encoder and decoder
import http # HTTP status codes
import os # Miscellaneous operating system interfaces

# import Django modules
from django.shortcuts import render # Render a template
from django.http import JsonResponse # JSON response
from django.template import loader # Load a template
from django.forms.models import model_to_dict # Convert a model instance to a dictionary
from django.views.decorators.http import require_POST # Require POST method
from django.db.models import Model # Django model
from django.conf import settings # Django settings

# import models
from user.models import Session # Session model
from api.models import ApiLink # API link model

# import utils
from . import utils

# Function to convert a model instance to a JSON object
# :param model: Django model instance
# :return: JSON object
def model_to_json(model: Model):
	target_dict = model_to_dict(model) # Convert model instance to dictionary
	result = {} # Initialize result dictionary
	for key in target_dict.keys(): # Iterate over dictionary keys
		result[key] = target_dict[key] # Add key-value pair to result dictionary
	try: # Try to get token from model
		result['token'] = model.token # Add token to result dictionary
	except: # Catch exceptions
		pass # Do nothing
	try: # Try to get name from model
		result['name'] = model.name # Add name to result dictionary
	except: # Catch exceptions
		pass # Do nothing
	if 'id' in result: # Check if 'id' key exists in result dictionary
		del result['id'] # Delete 'id' key from result dictionary
	if 'password' in result: # Check if 'password' key exists in result dictionary
		del result['password'] # Delete 'password' key from result dictionary
	return result # Return result dictionary

# Function to render the components page
# :param request: HTTP request
# :return: HTTP response
@require_POST # Require POST method
def server_data(request):
	apps = { # Initialize apps dictionary
		'/': 'front', # Frontend app
		'/user/': 'user', # User app
		'/api/': 'api', # API app
	} # Apps dictionary
	data = { # Initialize data dictionary
		'components': {}, # Components dictionary
		'selected': '/' # Selected path
	} # Data dictionary
	for app in apps: # Iterate over apps
		data['components'][app] = utils.get_templates(apps[app]) # Get templates for app
	token = request.COOKIES.get('token') # Get token from cookies
	session = Session.objects.select_related('user').filter(session_token=token).first() # Get session from token
	if token and session: # Check if token and session exist
		data['selected'] = '/user/' # Set selected path to '/user/'
	return JsonResponse(data, status=200) # Return JSON response

# Function to render the main page
# :param request: HTTP request
# :return: HTTP response
def main(request):
	template_path = os.path.join(settings.BASE_DIR, 'front', 'templates') # Get template path
	token = request.COOKIES.get('token') # Get token from cookies
	session = Session.objects.select_related('user').filter(session_token=token).first() # Get session from token
	json_data = {} # Initialize JSON data
	api_links = ApiLink.objects.all() # Get all API links
	json_data['api_links'] = [model_to_json(link) for link in api_links] # Convert API links to JSON objects
	if token and session: # Check if token and session exist
		json_data['userdata'] = model_to_json(session.user) # Convert user model to JSON object
		json_data['MEDIA_URL'] = settings.MEDIA_URL # Get media URL from settings
	if request.method != 'POST': # Check if request method is not POST
		try: # Try to render template
			return render(request, 'main.html', context=json_data) # Render main page
		except: # Catch exceptions
			return JsonResponse({'error': http.HTTPStatus(404).phrase}, status=404) # Return error response
	if request.body == None or request.body == b'': # Check if request body is empty
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400) # Return error response
	body = json.loads(request.body) # Load JSON data from request body
	fields = ['type', 'file'] # Initialize fields
	if 'data' in body.keys() and body['data']:
		fields.append('data')
	if set(fields) != set(body.keys()): # Check if fields are not in body
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400) # Return error response
	valid_types = ['navbar', 'content', 'modal', 'footer'] # Initialize valid types
	if body['type'] not in valid_types: # Check if type is not in valid types
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400) # Return error response
	if not body['file']: # Check if file is empty
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400) # Return error response
	try: # Try to render template
		html = loader.render_to_string(os.path.join(template_path, f'{body["file"]}.html'), context=json_data) # Render template
		return JsonResponse({ # Return JSON response
			'success': http.HTTPStatus(200).phrase, # Success message
			'html': html # HTML data
		}, status=200) # Return success response
	except: # Catch exceptions
		return JsonResponse({'error': http.HTTPStatus(404).phrase}, status=404) # Return error response

