from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .models import Users
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password

# Create your views here.
def parse_name(name):
	name = name.strip()
	if len(name) < 3:
		return None
	if len(name) > 32:
		return None
	if not name.isalpha():
		return None
	return name.capitalize()

def parse_username(username):
	username = username.strip()
	if len(username) < 3:
		return None
	if len(username) > 32:
		return None
	for i in range(len(username)):
		if username[i].isupper():
			return None
		if username[i] in '-_.' or username[i].isalnum():
			continue
		return None
	if not username[0].isalnum():
		return None
	return username

def parse_email(email):
	email = email.strip()
	if len(email) < 5:
		return None
	if len(email) > 97:
		return None
	main_values = email.split('@')
	at_count = email.count('@')
	main_count = len(main_values)
	if main_count != 2 or at_count != main_count - 1:
		return None
	if parse_username(main_values[0]) == None:
		return None
	domain_values = main_values[1].split('.')
	dot_count = main_values[1].count('.')
	domain_count = len(domain_values)
	if domain_count < 2 or dot_count != domain_count - 1:
		return None
	if len(main_values[1]) < 2:
		return None
	if len(main_values[1]) > 64:
		return None
	for i in range(domain_count):
		if not domain_values[i].isalnum():
			return None
	return main_values[0] + '@' + main_values[1]

def parse_password(password):
	password = password.strip()
	if len(password) < 8:
		return None
	if len(password) > 32:
		return None
	if password.isspace():
		return None
	if not any(char.isdigit() for char in password):
		return None
	if not any(char.islower() for char in password):
		return None
	if not any(char.isupper() for char in password):
		return None
	if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?/' for char in password):
		return None
	return make_password(password)

@csrf_exempt
def signup(request):
	if (request.method != 'POST'):
		return redirect('/')
	data = json.loads(request.body)
	results = []
	for key in data:
		if key == 'fname' or key == 'lname':
			results.append(parse_name(data[key]))
		elif key == 'username':
			results.append(parse_username(data[key]))
		elif key == 'email':
			results.append(parse_email(data[key]))
		elif key == 'password':
			results.append(parse_password(data[key]))
	for result in results:
		if result == None:
			return JsonResponse({'error': 'Invalid data'})
	Users.objects.all().delete()
	users = Users.objects.all()
	for user in users:
		if user.username == data['username']:
			return JsonResponse({'error': 'Username already exists'})
		if user.email == data['email']:
			return JsonResponse({'error': 'Email already exists'})
	Users.objects.create(
		fname=parse_name(data['fname']),
		lname=parse_name(data['lname']),
		username=parse_username(data['username']),
		email=parse_email(data['email']),
		password=parse_password(data['password'])
	)
	return JsonResponse({'success': 'User created'})
