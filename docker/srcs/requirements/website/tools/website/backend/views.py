import http, os, json
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from django.core.files.storage import default_storage
from rest_framework.authtoken.models import Token
from . import parse
from .models import Users, Sessions

# Create your views here.
@require_POST
def signup(request):
	body = {}
	for key in request.POST:
		body[key] = request.POST[key]
	if body == {}:
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400)
	fields = ['fname', 'lname', 'username', 'email', 'password']
	if set(fields) != set(body.keys()):
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400)
	file = {}
	for key in request.FILES:
		file[key] = request.FILES[key]
	if file == {}:
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400)
	file_fields = ['profilephoto']
	if set(file_fields) != set(file.keys()):
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400)
	if not file['profilephoto'].content_type.startswith('image/'):
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400)
	parsing = {
		'fname': parse.name(body['fname']),
		'lname': parse.name(body['lname']),
		'username': parse.username(body['username']),
		'email': parse.email(body['email']),
		'password': parse.password(body['password']),
	}
	if None in parsing.values():
		return JsonResponse({'error': http.HTTPStatus(401).phrase}, status=401)
	target = Users.objects.filter(
		Q(username=parsing['username']) | Q(email=parsing['email'])
	).first()
	if target:
		return JsonResponse({'error': http.HTTPStatus(401).phrase}, status=401)
	_, ext = os.path.splitext(file['profilephoto'].name)
	new_filename = f"{parsing['username']}{ext}"
	default_storage.save('static/profilephotos/' + new_filename, file['profilephoto'])
	user = Users.objects.create(
		fname=parsing['fname'],
		lname=parsing['lname'],
		username=parsing['username'],
		password=parsing['password'],
		email=parsing['email'],
		profilephoto=new_filename
	)
	token = RefreshToken.for_user(user)
	Sessions.objects.create(user_id=user.id, session_token=token)
	response = JsonResponse({'success': http.HTTPStatus(201).phrase}, status=201)
	response.set_cookie('token', str(token), samesite='Strict', secure=True)
	return response

@require_POST
def signin(request):
	cookies = {}
	for key in request.COOKIES:
		cookies[key] = request.COOKIES[key]
	if 'token' in cookies.keys():
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400)
	body = json.loads(request.body)
	if body == {}:
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400)
	fields = ['username', 'password']
	if set(fields) != set(body.keys()):
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400)
	user = Users.objects.filter(username=body['username']).first()
	if not user or not check_password(body['password'], user.password):
		return JsonResponse({'error': http.HTTPStatus(401).phrase}, status=401)
	token = RefreshToken.for_user(user)
	Sessions.objects.create(user_id=user.id, session_token=token)
	response = JsonResponse({'success': http.HTTPStatus(200).phrase}, status=200)
	response.set_cookie('token', str(token), samesite='Strict', secure=True)
	return response

@require_POST
def signout(request):
	cookies = {}
	for key in request.COOKIES:
		cookies[key] = request.COOKIES[key]
	if 'token' not in cookies.keys():
		return JsonResponse({'error': http.HTTPStatus(401).phrase}, status=401)
	Sessions.objects.filter(session_token=cookies['token']).delete()
	response = JsonResponse({'success': http.HTTPStatus(200).phrase}, status=200)
	response.delete_cookie('token')
	return response
