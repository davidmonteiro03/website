from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json
from . import parse
from .models import Users
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
@require_POST
def signup(request):
	Users.objects.all().delete()
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
	user.token = RefreshToken.for_user(user)
	user.save()
	return JsonResponse({'token': str(user.token)})
