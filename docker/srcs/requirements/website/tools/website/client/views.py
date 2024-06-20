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
	fields = ['type', 'file', 'data'] # Initialize fields
	if set(fields) != set(body.keys()): # Check if fields are not in body
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400) # Return error response
	valid_types = ['navbar', 'app', 'modal', 'footer'] # Initialize valid types
	if body['type'] not in valid_types: # Check if type is not in valid types
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400) # Return error response
	if not body['file']: # Check if file is empty
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400) # Return error response
	if body['data']: # Check if data exists
		json_data['req_data'] = body['data'] # Add data to JSON data
	json_data['api_data'] = {} # Initialize API data
	try: # Try to get API data
		response = requests.get(f'http://localhost:5000/api/{body["file"]}/') # Send GET request to API
		resp_data = response.json() # Get JSON data from response
		json_data['api_data'][body['file']] = resp_data['content'] # Add API data to JSON data
	except: # Catch exceptions
		pass # Pass
	try: # Try to render template
		html = loader.render_to_string(f'{body["file"]}.html', context=json_data) # Render template
		return JsonResponse({ # Return JSON response
			'success': http.HTTPStatus(200).phrse, # Success message
			'html': html # HTML data
		}, status=200) # Return success response
	except: # Catch exceptions
		return JsonResponse({'error': http.HTTPStatus(404).phrase}, status=404) # Return error response
