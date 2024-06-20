# import Python modules
import json # JSON encoder and decoder
import http # HTTP status codes
import requests # HTTP requests

# import Django modules
from django.shortcuts import render # Render a template
from django.http import JsonResponse # JSON response
from django.template import loader # Load a template
from django.forms.models import model_to_dict # Convert a model instance to a dictionary
from django.db.models import Model # Django model
from django.db.models import Q # Django query
from django.conf import settings # Django settings

# import models
from authentication.models import Session # Session model
from api.models import ApiLink # ApiLink model

# Function to convert a model instance to a JSON object
# :param model: Django model instance
# :return: JSON object
def model_to_json(model: Model):
	target_dict = model_to_dict(model) # Convert model instance to dictionary
	result = {} # Initialize result dictionary
	for key in target_dict.keys(): # Iterate over dictionary keys
		result[key] = target_dict[key] # Add key-value pair to result dictionary
	try: # Try to get token
		result['token'] = model.token # Add token to result dictionary
	except: # Catch exceptions
		pass # Do nothing
	if 'id' in result: # Check if 'id' key exists in result dictionary
		del result['id'] # Delete 'id' key from result dictionary
	if 'password' in result: # Check if 'password' key exists in result dictionary
		del result['password'] # Delete 'password' key from result dictionary
	return result # Return result dictionary

# Function to render the main page
# :param request: HTTP request
# :return: HTTP response
def main(request):
	token = request.COOKIES.get('token') # Get token from cookies
	session = Session.objects.select_related('user').filter(session_token=token).first() # Get session from token
	json_data = {} # Initialize JSON data
	if token and session: # Check if token and session exist
		json_data['userdata'] = model_to_json(session.user) # Convert user model to JSON object
		json_data['api_links'] = [model_to_json(link) for link in ApiLink.objects.all()] # Convert API links to JSON objects
		if not json_data['api_links']: # Check if API links exist
			del json_data['api_links'] # Delete API links from JSON data
		json_data['MEDIA_URL'] = settings.MEDIA_URL # Get media URL from settings
	if request.method != 'POST': # Check if request method is not POST
		return render(request, 'main.html', context=json_data) # Render main page
	if request.body == None or request.body == b'': # Check if request body is empty
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400) # Return error response
	body = json.loads(request.body) # Load JSON data from request body
	fields = ['type', 'file'] # Initialize fields
	if 'api_data' in body.keys(): # Check if 'api_data' key exists in body
		fields.append('api_data')
	if set(fields) != set(body.keys()): # Check if fields are not in body
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400) # Return error response
	valid_types = ['navbar', 'app', 'modal', 'footer'] # Initialize valid types
	if body['type'] not in valid_types: # Check if type is not in valid types
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400) # Return error response
	if not body['file']: # Check if file is empty
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400) # Return error response
	if body['type'] != 'app':
		try:
			html = loader.render_to_string(f'{body["file"]}.html', context=json_data) # Render template
			return JsonResponse({ # Return JSON response
				'success': http.HTTPStatus(200).phrase, # Success message
				'html': html # HTML data
			}, status=200) # Return success response
		except:
			return JsonResponse({'error': http.HTTPStatus(404).phrase}, status=404)
	if 'api_data' in body.keys(): # Check if 'api_data' key exists in body
		try: # Try to get API data
			api_model_target = ApiLink.objects.filter(
				Q(link=body['file']) & Q(token=body['api_data']) # for now I can't use json sintax in django templates so it gets strings
				# Q(link=body['file']) & Q(token=body['api_data']['token']) # in the future, if I could use json sintax in django templates, I would use this line
			).first() # Get API model target
			if not api_model_target: # Check if API model target does not exist
				raise Exception # Raise exception
			json_data['api_data'] = {} # Initialize API data
			response = requests.get(f'http://localhost:{request.META["SERVER_PORT"]}/api/{body["file"]}/') # Send GET request to API
			resp_data = response.json() # Get JSON data from response
			json_data['api_data'][body['file']] = resp_data['content'] # Add API data to JSON data
			html = loader.render_to_string(f'{body["file"]}.html', context=json_data) # Render template
			return JsonResponse({ # Return JSON response
				'success': http.HTTPStatus(200).phrase, # Success message
				'html': html # HTML data
			}, status=200) # Return success response
		except: # Catch exceptions
			return JsonResponse({'error': http.HTTPStatus(404).phrase}, status=404) # Return error response
	try: # Try to render template
		api_model_target = ApiLink.objects.filter(link=body['file']).first() # Get API model target
		if api_model_target: # Check if API model target does not exist
			raise Exception # Raise exception
		html = loader.render_to_string(f'{body["file"]}.html', context=json_data) # Render template
		return JsonResponse({ # Return JSON response
			'success': http.HTTPStatus(200).phrase, # Success message
			'html': html # HTML data
		}, status=200) # Return success response
	except: # Catch exceptions
		return JsonResponse({'error': http.HTTPStatus(404).phrase}, status=404) # Return error response

