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
			return JsonResponse(None, safe=False, status=400)
	Users.objects.all().delete()
	users = Users.objects.all()
	for user in users:
		if user.username == data['username']:
			return JsonResponse(None, safe=False, status=400)
		if user.email == data['email']:
			return JsonResponse(None, safe=False, status=400)
	Users.objects.create(
		fname=parse.name(data['fname']),
		lname=parse.name(data['lname']),
		username=parse.username(data['username']),
		email=parse.email(data['email']),
		password=parse.password(data['password'])
	)
	return_data = {
		'fname': parse.name(data['fname']),
		'lname': parse.name(data['lname']),
		'username': parse.username(data['username']),
		'email': parse.email(data['email'])
	}
	return JsonResponse(return_data)

@csrf_exempt
def update(request):
	if (request.method != 'POST'):
		return redirect('/')
	if not request.body or request.body == b'{}':
		return JsonResponse(None, safe=False, status=400)
	print(request.body)
	data = json.loads(request.body)
	user = Users.objects.filter(username=data['username']).first()
	if user:
		user.fname = data['fname']
		user.lname = data['lname']
		user.save()
		return_data = {
			'fname': user.fname,
			'lname': user.lname,
			'username': user.username,
			'email': user.email
		}
		return JsonResponse(return_data)
	return JsonResponse(None, safe=False, status=404)
