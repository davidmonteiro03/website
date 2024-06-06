from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json
from . import parse

# Create your views here.
@require_POST
def signup(request):
	if (request.body == None or request.body == b''):
		return JsonResponse(None, safe=False, status=400)
	body = json.loads(request.body)
	fields = ['fname', 'lname', 'username', 'email', 'password']
	for key in body:
		if key not in fields:
			return JsonResponse(None, safe=False, status=400)
	parsing = {
		'fname': parse.name(body['fname']),
		'lname': parse.name(body['lname']),
		'username': parse.username(body['username']),
		'email': parse.email(body['email']),
		'password': parse.password(body['password']),
	}
	if None in parsing.values():
		return JsonResponse(None, safe=False, status=401)
	print(parsing)
	return JsonResponse(None, safe=False)
