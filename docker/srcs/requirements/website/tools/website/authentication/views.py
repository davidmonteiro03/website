from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .models import Users
from django.views.decorators.csrf import csrf_exempt
from . import parse
from django.db import connection
from django.db.models import Q

# Create your views here
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
	target = Users.objects.filter(
		Q(username=data['username']) | Q(email=data['email'])
	).first()
	if target:
		return JsonResponse(None, safe=False, status=400)
	return_data = {
		'fname': parse.name(data['fname']),
		'lname': parse.name(data['lname']),
		'username': parse.username(data['username']),
		'email': parse.email(data['email'])
	}
	Users.objects.create(
		fname=parse.name(data['fname']),
		lname=parse.name(data['lname']),
		username=parse.username(data['username']),
		email=parse.email(data['email']),
		password=parse.password(data['password'])
	)
	return JsonResponse(return_data)

def update(request):
	if (request.method != 'POST'):
		return redirect('/')
	if not request.body or request.body == b'{}':
		return JsonResponse(None, safe=False, status=400)
	in_data = json.loads(request.body)
	target = Users.objects.filter(
		username=in_data['user_data']['username'],
		email=in_data['user_data']['email']
	).first()
	if not target:
		return JsonResponse(None, safe=False, status=400)
	values = {
		'fname': parse.name(in_data['new_data']['fname']),
		'lname': parse.name(in_data['new_data']['lname']),
		'username': parse.username(in_data['new_data']['username']),
		'email': parse.email(in_data['new_data']['email']),
	}
	target = Users.objects.filter(
		username=in_data['user_data']['username'],
		email=in_data['user_data']['email']
	).first()
	for key in in_data['new_data']:
		if values[key] and values[key] != target.__dict__[key]:
			target.__dict__[key] = values[key]
	target.save()
	out_data = {
		'fname': target.fname,
		'lname': target.lname,
		'username': target.username,
		'email': target.email
	}
	return JsonResponse(out_data)
