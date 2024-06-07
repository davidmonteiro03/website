from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
import json
from . import parse
from .models import Users
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password

# Create your views here.
@require_POST
def signup(request):
	if (request.body == None or request.body == b''):
		return JsonResponse(None, safe=False, status=400)
	body = json.loads(request.body)
	fields = ['fname', 'lname', 'username', 'email', 'password']
	if set(fields) != set(body.keys()):
		return JsonResponse(None, safe=False, status=400)
	parsing = {
		'fname': parse.name(body['fname']),
		'lname': parse.name(body['lname']),
		'username': parse.username(body['username']),
		'email': parse.email(body['email']),
		'password': parse.password(body['password']),
	}
	target = Users.objects.filter(
		Q(username=parsing['username']) | Q(email=parsing['email'])
	).first()
	if target is not None or None in parsing.values():
		return JsonResponse(None, safe=False, status=401)
	user = Users.objects.create(
		fname=parsing['fname'],
		lname=parsing['lname'],
		username=parsing['username'],
		email=parsing['email'],
		password=parsing['password'],
	)
	sessiontoken = RefreshToken.for_user(user)
	response = JsonResponse({
		'sessiontoken': str(sessiontoken),
		'publicdata': {
			'fname': user.fname,
			'lname': user.lname,
			'username': user.username,
			'email': user.email
		}
	})
	response.set_cookie('sessiontoken', str(sessiontoken), samesite='Strict', secure=True)
	user.sessiontoken = response.cookies['sessiontoken'].value
	user.save()
	return response

@require_POST
def signout(request):
	if (request.body == None or request.body == b''):
		return JsonResponse(None, safe=False, status=400)
	body = json.loads(request.body)
	fields = ['sessiontoken']
	if set(fields) != set(body.keys()):
		return JsonResponse(None, safe=False, status=400)
	if 'sessiontoken' not in body:
		return JsonResponse(None, safe=False, status=400)
	target = Users.objects.filter(sessiontoken=body['sessiontoken']).first()
	if not target:
		return JsonResponse(None, safe=False, status=401)
	if target.sessiontoken == '':
		return JsonResponse(None, safe=False, status=401)
	respose = JsonResponse({'success': 'true'})
	respose.delete_cookie('sessiontoken', samesite='Strict')
	target.sessiontoken = ''
	target.save()
	return respose

@require_POST
def signin(request):
	if (request.body == None or request.body == b''):
		return JsonResponse(None, safe=False, status=400)
	body = json.loads(request.body)
	fields = ['username', 'password']
	if set(fields) != set(body.keys()):
		return JsonResponse(None, safe=False, status=400)
	target = Users.objects.filter(username=body['username']).first()
	if not target:
		return JsonResponse(None, safe=False, status=401)
	if not check_password(body['password'], target.password):
		return JsonResponse(None, safe=False, status=401)
	sessiontoken = RefreshToken.for_user(target)
	response = JsonResponse({
		'sessiontoken': str(sessiontoken),
		'publicdata': {
			'fname': target.fname,
			'lname': target.lname,
			'username': target.username,
			'email': target.email
		}
	})
	response.set_cookie('sessiontoken', str(sessiontoken), samesite='Strict', secure=True)
	target.sessiontoken = response.cookies['sessiontoken'].value
	target.save()
	return response
