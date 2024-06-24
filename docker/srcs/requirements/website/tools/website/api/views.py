# import Python modules
import json # JSON encoder and decoder
import http # HTTP status codes
import os # Miscellaneous operating system interfaces

# import Django modules
from django.http import JsonResponse # JSON response
from django.template import loader # Load a template
from django.forms.models import model_to_dict # Convert a model instance to a dictionary
from django.views.decorators.http import require_POST # Require POST method
from django.db.models import Model # Django model
from django.conf import settings # Django settings

# import models
from user.models import Session # Session model
from api.models import ApiLink # API link model

# import api
from . import api

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
	if 'id' in result: # Check if 'id' key exists in result dictionary
		del result['id'] # Delete 'id' key from result dictionary
	return result # Return result dictionary

# Function to render template
# :param request: HTTP request
# :return: HTTP response
@require_POST # Require POST method
def main(request):
	token = request.COOKIES.get('token') # Get token from cookies
	session = Session.objects.select_related('user').filter(session_token=token).first() # Get session from token
	private_path = os.path.join(settings.BASE_DIR, 'user', 'templates') # Get private path from settings
	public_path = os.path.join(settings.BASE_DIR, 'front', 'templates') # Get public path from settings
	template_path = os.path.join(settings.BASE_DIR, 'api', 'templates') # Get template path from settings
	json_data = {} # Initialize JSON data
	api_links = ApiLink.objects.all() # Get all API links
	json_data['api_links'] = [model_to_json(link) for link in api_links] # Convert API links to JSON objects
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
		if body['type'] == 'navbar' or body['type'] == 'modal': # Check if type is navbar or modal
			if token and session: # Check if token and session exist
				html = loader.render_to_string(os.path.join(private_path, f'{body["file"]}.html'), context=json_data) # Render private template
			else: # Otherwise
				html = loader.render_to_string(os.path.join(public_path, f'{body["file"]}.html'), context=json_data) # Render public template
		else: # Otherwise
			find_link = ApiLink.objects.filter(token=body['data']).first() # Find API link
			if find_link and find_link.link in api.__dict__:
				json_data['api_data'] = {}
				json_data['api_data'][find_link.link] = api.__dict__[find_link.link]()
				html = loader.render_to_string(os.path.join(template_path, f'{body["file"]}.html'), context=json_data) # Render template
			else:
				if body['type'] == 'app':
					html = loader.render_to_string(os.path.join(template_path, 'index.html'), context=json_data) # Render template
				else:
					html = loader.render_to_string(os.path.join(template_path, f'{body["file"]}.html'), context=json_data)
		return JsonResponse({ # Return JSON response
			'success': http.HTTPStatus(200).phrase, # Success message
			'html': html # HTML data
		}, status=200) # Return success response
	except: # Catch exceptions
		return JsonResponse({'error': http.HTTPStatus(404).phrase}, status=404) # Return error response
