# import Python modules
import http # HTTP status codes
import json # JSON encoder and decoder
import os # Miscellaneous operating system interfaces
from rest_framework_simplejwt.tokens import RefreshToken # Refresh token

# import Django modules
from django.views.decorators.http import require_POST # Require POST method
from django.http import JsonResponse # JSON response
from django.db.models import Q # Django query
from django.contrib.auth.hashers import check_password # Check password
from django.core.files.storage import default_storage # Default storage
from django.template import loader # Template loader
from django.forms.models import model_to_dict # Convert a model instance to a dictionary
from django.db.models import Model # Django model
from django.conf import settings # Django settings

# import parse
from . import parse

# import models
from .models import User # User model
from .models import Session # Session model

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

# Function to main
# :param request: HTTP request
# :return: JSON response
@require_POST # Require POST method
def main(request):
	cookies = {} # Empty dictionary
	for key in request.COOKIES: # Iterate over cookies
		cookies[key] = request.COOKIES[key] # Add cookies to dictionary
	if cookies == {} or 'token' not in cookies.keys(): # Check if cookies is empty or token is not in cookies
		return JsonResponse({'error': http.HTTPStatus(401).phrase}, status=401) # Return error
	template_path = os.path.join(settings.BASE_DIR, 'user', 'templates') # Get template path from settings
	token = request.COOKIES.get('token') # Get token from cookies
	session = Session.objects.select_related('user').filter(session_token=token).first() # Get session from token
	json_data = {} # Initialize JSON data
	if not token or not session: # Check if token and session exist
		return JsonResponse({'error': http.HTTPStatus(401).phrase}, status=401) # Return error
	json_data['userdata'] = model_to_json(session.user) # Convert user model to JSON object
	json_data['MEDIA_URL'] = settings.MEDIA_URL # Get media URL from settings
	if request.body == None or request.body == b'': # Check if request body is empty
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400) # Return error response
	body = json.loads(request.body) # Load JSON data from request body
	fields = ['type', 'file'] # Initialize fields
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

# Function to sign up
# :param request: HTTP request
# :return: JSON response
@require_POST # Require POST method
def signup(request):
	body = {} # Empty dictionary
	for key in request.POST: # Iterate over POST request
		body[key] = request.POST[key] # Add POST request to body
	if body == {}: # Check if body is empty
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400) # Return error
	fields = ['fname', 'lname', 'username', 'email', 'password'] # Fields
	if set(fields) != set(body.keys()): # Check if fields are not in body
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400) # Return error
	file = {} # Empty dictionary
	for key in request.FILES: # Iterate over FILES request
		file[key] = request.FILES[key] # Add FILES request to file
	if file == {}: # Check if file is empty
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400) # Return error
	file_fields = ['profilephoto'] # File fields
	if set(file_fields) != set(file.keys()): # Check if file fields are not in file
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400) # Return error
	if not file['profilephoto'].content_type.startswith('image/'): # Check if content type is not image
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400) # Return error
	parsing = { # Parsing
		'fname': parse.name(body['fname']), # Parse first name
		'lname': parse.name(body['lname']), # Parse last name
		'username': parse.username(body['username']), # Parse username
		'email': parse.email(body['email']), # Parse email
		'password': parse.password(body['password']), # Parse password
	}
	if None in parsing.values(): # Check if None is in parsing values
		return JsonResponse({'error': http.HTTPStatus(401).phrase}, status=401) # Return error
	if User.objects.filter(Q(username=parsing['username']) | Q(email=parsing['email'])).exists(): # Check if user exists
		return JsonResponse({'error': http.HTTPStatus(401).phrase}, status=401) # Return error
	user = User.objects.create( # Create user
		fname=parsing['fname'], # First name
		lname=parsing['lname'], # Last name
		username=parsing['username'], # Username
		password=parsing['password'], # Password
		email=parsing['email'], # Email
		profilephoto=file['profilephoto'] # Profile photo
	)
	token = RefreshToken.for_user(user) # Refresh token for user
	Session.objects.create(user_id=user.id, session_token=token) # Create session
	response = JsonResponse({'success': http.HTTPStatus(201).phrase}, status=201) # JSON response
	response.set_cookie('token', str(token), samesite='Strict', secure=True) # Set cookie
	return response # Return response

# Function to sign in
# :param request: HTTP request
# :return: JSON response
@require_POST # Require POST method
def signin(request):
	cookies = {} # Empty dictionary
	for key in request.COOKIES: # Iterate over cookies
		cookies[key] = request.COOKIES[key] # Add cookies to dictionary
	if cookies == {} or 'token' in cookies.keys(): # Check if cookies is empty or token is in cookies
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400) # Return error
	if request.body == b'': # Check if body is empty
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400) # Return error
	body = json.loads(request.body) # Load body
	if body == {}: # Check if body is empty
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400) # Return error
	fields = ['username', 'password'] # Fields
	if set(fields) != set(body.keys()): # Check if fields are not in body
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400) # Return error
	user = User.objects.filter(username=body['username']).first() # Filter user
	if not user or not check_password(body['password'], user.password): # Check if user does not exist or password is incorrect
		return JsonResponse({'error': http.HTTPStatus(401).phrase}, status=401) # Return error
	token = RefreshToken.for_user(user) # Refresh token for user
	Session.objects.create(user_id=user.id, session_token=token) # Create session
	response = JsonResponse({'success': http.HTTPStatus(200).phrase}, status=200) # JSON response
	response.set_cookie('token', str(token), samesite='Strict', secure=True) # Set cookie
	return response # Return response

# Function to sign out
# :param request: HTTP request
# :return: JSON response
@require_POST # Require POST method
def signout(request):
	cookies = {} # Empty dictionary
	for key in request.COOKIES: # Iterate over cookies
		cookies[key] = request.COOKIES[key] # Add cookies to dictionary
	if cookies == {} or 'token' not in cookies.keys(): # Check if cookies is empty or token is not in cookies
		return JsonResponse({'error': http.HTTPStatus(401).phrase}, status=401) # Return error
	Session.objects.filter(session_token=cookies['token']).delete() # Delete session
	response = JsonResponse({'success': http.HTTPStatus(200).phrase}, status=200) # JSON response
	response.delete_cookie('token') # Delete cookie
	return response # Return response

# Function to get user
# :param request: HTTP request
# :return: JSON response
@require_POST # Require POST method
def getuser(request):
	if request.body == b'': # Check if body is empty
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400) # Return error
	body = json.loads(request.body) # Load body
	if len(body) != 1: # Check if length is not 1
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400) # Return error
	valid_fields = ['username', 'email'] # Valid fields
	field = list(body.keys())[0] # Field
	if field not in valid_fields: # Check if field is not in valid fields
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400) # Return error
	target = User.objects.filter(Q(username=body[field]) | Q(email=body[field])).first() # Filter target
	if target: # Check if target exists
		return JsonResponse({'error': http.HTTPStatus(401).phrase}, status=401) # Return error
	return JsonResponse({'success': http.HTTPStatus(200).phrase}, status=200) # Return success

# Function to update user
# :param request: HTTP request
# :return: JSON response
@require_POST # Require POST method
def update(request): # Update user
	cookies = {} # Empty dictionary
	for key in request.COOKIES: # Iterate over cookies
		cookies[key] = request.COOKIES[key] # Add cookies to dictionary
	if 'token' not in cookies.keys(): # Check if token is not in cookies
		return JsonResponse({'error': http.HTTPStatus(401).phrase}, status=401) # Return error
	session = Session.objects.select_related('user').filter(session_token=cookies['token']).first() # Filter session
	if not session: # Check if session does not exist
		return JsonResponse({'error': http.HTTPStatus(401).phrase}, status=401) # Return error
	soft_fields = ['fname', 'lname'] # Soft fields
	hard_fields = ['username', 'oldpassword', 'newpassword'] # Hard fields
	fields = soft_fields + hard_fields # Fields
	body = {} # Empty dictionary
	for key in request.POST: # Iterate over POST request
		body[key] = request.POST[key] # Add POST request to body
	if not request.FILES: # Check if FILES request is empty
		del body['profilephoto'] # Delete profile photo
	if set(fields) != set(body.keys()): # Check if fields are not in body
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400) # Return error
	user = session.user # User
	parsers = { # Parsers
		'fname': parse.name, 'lname': parse.name, # First and last name
		'username': parse.username, # Parse username
		'oldpassword': parse.password, 'newpassword': parse.password # Parse old and new password
	}
	for key in soft_fields: # Iterate over soft fields
		if parsers[key](body[key]) and user.__dict__[key] != parsers[key](body[key]): # Check if parser is valid and user is not equal to parser
			user.__dict__[key] = parsers[key](body[key]) # Set user to parser
	if parsers[hard_fields[0]](body[hard_fields[0]]) and user.username != parsers[hard_fields[0]](body[hard_fields[0]]): # Check if parser is valid and user is not equal to parser
		target = User.objects.filter(username=parsers[hard_fields[0]](body[hard_fields[0]])).first() # Filter target
		if not target: # Check if target does not exist
			user.username = parsers[hard_fields[0]](body[hard_fields[0]]) # Set username
	if request.FILES: # Check if FILES request exists
		file = {} # Empty dictionary
		for key in request.FILES: # Iterate over FILES request
			file[key] = request.FILES[key] # Add FILES request to file
		if 'profilephoto' in file.keys() and file['profilephoto'].content_type.startswith('image/'): # Check if profile photo is in file keys and content type is image
			if user.profilephoto != file['profilephoto']: # Check if profile photo is not equal to file
				default_storage.delete(user.profilephoto.name) # Delete profile photo
				user.profilephoto = file['profilephoto'] # Set profile photo
	if parsers[hard_fields[1]](body[hard_fields[1]]) and check_password(body[hard_fields[1]], user.password) and not check_password(body[hard_fields[2]], user.password): # Check if parser is valid, password is correct, and new password is not correct
		user.password = parsers[hard_fields[2]](body[hard_fields[2]]) # Set password
	user.save() # Save user
	return JsonResponse({'success': http.HTTPStatus(200).phrase}, status=200) # Return success
