from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .models import Users
from django.views.decorators.csrf import csrf_exempt
from . import parse

# Create your views here
@csrf_exempt
def signup(request):
	if (request.method != 'POST'):
		return redirect('/')
	data = json.loads(request.body)
	results = []
	for key in data:
		if key == 'fname' or key == 'lname':
			results.append(parse.name(data[key]))
		elif key == 'username':
			results.append(parse.username(data[key]))
		elif key == 'email':
			results.append(parse.email(data[key]))
		elif key == 'password':
			results.append(parse.password(data[key]))
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
		fname=parse.name(data['fname']),
		lname=parse.name(data['lname']),
		username=parse.username(data['username']),
		email=parse.email(data['email']),
		password=parse.password(data['password'])
	)
	return JsonResponse({'success': 'User created'})
