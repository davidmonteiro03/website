# import Python modules
import http # HTTP status codes
import json # JSON encoder and decoder
from rest_framework_simplejwt.tokens import RefreshToken # Refresh token

# import Django modules
from django.views.decorators.http import require_POST # Require POST method
from django.http import JsonResponse # JSON response
from django.db.models import Q # Django query
from django.contrib.auth.hashers import check_password # Check password
from django.core.files.storage import default_storage # Default storage

# import parse
from . import parse

# import models
from .models import User # User model
from .models import Session # Session model

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
