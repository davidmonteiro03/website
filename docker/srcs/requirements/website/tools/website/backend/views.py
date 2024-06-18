import http, json, requests
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from django.core.files.storage import default_storage
from . import parse
from .models import User, Session
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.
@require_POST
@ensure_csrf_cookie
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
	if User.objects.filter(Q(username=parsing['username']) | Q(email=parsing['email'])).exists():
		return JsonResponse({'error': http.HTTPStatus(401).phrase}, status=401)
	user = User.objects.create(
		fname=parsing['fname'],
		lname=parsing['lname'],
		username=parsing['username'],
		password=parsing['password'],
		email=parsing['email'],
		profilephoto=file['profilephoto']
	)
	token = RefreshToken.for_user(user)
	Session.objects.create(user_id=user.id, session_token=token)
	response = JsonResponse({'success': http.HTTPStatus(201).phrase}, status=201)
	response.set_cookie('token', str(token), samesite='Strict', secure=True)
	return response

@require_POST
@ensure_csrf_cookie
def signin(request):
	cookies = {}
	for key in request.COOKIES:
		cookies[key] = request.COOKIES[key]
	if cookies == {} or 'token' in cookies.keys():
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400)
	if request.body == b'':
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400)
	body = json.loads(request.body)
	if body == {}:
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400)
	fields = ['username', 'password']
	if set(fields) != set(body.keys()):
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400)
	user = User.objects.filter(username=body['username']).first()
	if not user or not check_password(body['password'], user.password):
		return JsonResponse({'error': http.HTTPStatus(401).phrase}, status=401)
	token = RefreshToken.for_user(user)
	Session.objects.create(user_id=user.id, session_token=token)
	response = JsonResponse({'success': http.HTTPStatus(200).phrase}, status=200)
	response.set_cookie('token', str(token), samesite='Strict', secure=True)
	return response

@require_POST
@ensure_csrf_cookie
def signout(request):
	cookies = {}
	for key in request.COOKIES:
		cookies[key] = request.COOKIES[key]
	if cookies == {} or 'token' not in cookies.keys():
		return JsonResponse({'error': http.HTTPStatus(401).phrase}, status=401)
	Session.objects.filter(session_token=cookies['token']).delete()
	response = JsonResponse({'success': http.HTTPStatus(200).phrase}, status=200)
	response.delete_cookie('token')
	return response

@require_POST
@ensure_csrf_cookie
def getuser(request):
	if request.body == b'':
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400)
	body = json.loads(request.body)
	if len(body) != 1:
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400)
	valid_fields = ['username', 'email']
	field = list(body.keys())[0]
	if field not in valid_fields:
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400)
	target = User.objects.filter(Q(username=body[field]) | Q(email=body[field])).first()
	if target:
		return JsonResponse({'error': http.HTTPStatus(401).phrase}, status=401)
	return JsonResponse({'success': http.HTTPStatus(200).phrase}, status=200)

@require_POST
@ensure_csrf_cookie
def update(request):
	cookies = {}
	for key in request.COOKIES:
		cookies[key] = request.COOKIES[key]
	if 'token' not in cookies.keys():
		return JsonResponse({'error': http.HTTPStatus(401).phrase}, status=401)
	session = Session.objects.select_related('user').filter(session_token=cookies['token']).first()
	if not session:
		return JsonResponse({'error': http.HTTPStatus(401).phrase}, status=401)
	soft_fields = ['fname', 'lname']
	hard_fields = ['username', 'oldpassword', 'newpassword']
	fields = soft_fields + hard_fields
	body = {}
	for key in request.POST:
		body[key] = request.POST[key]
	if not request.FILES:
		del body['profilephoto']
	if set(fields) != set(body.keys()):
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400)
	user = session.user
	parsers = {
		'fname': parse.name, 'lname': parse.name,
		'username': parse.username,
		'oldpassword': parse.password, 'newpassword': parse.password
	}
	for key in soft_fields:
		if parsers[key](body[key]) and user.__dict__[key] != parsers[key](body[key]):
			user.__dict__[key] = parsers[key](body[key])
	if parsers[hard_fields[0]](body[hard_fields[0]]) and user.username != parsers[hard_fields[0]](body[hard_fields[0]]):
		target = User.objects.filter(username=parsers[hard_fields[0]](body[hard_fields[0]])).first()
		if not target:
			user.username = parsers[hard_fields[0]](body[hard_fields[0]])
	if request.FILES:
		file = {}
		for key in request.FILES:
			file[key] = request.FILES[key]
		if 'profilephoto' in file.keys() and file['profilephoto'].content_type.startswith('image/'):
			if user.profilephoto != file['profilephoto']:
				default_storage.delete(user.profilephoto.name)
				user.profilephoto = file['profilephoto']
	if parsers[hard_fields[1]](body[hard_fields[1]]) and check_password(body[hard_fields[1]], user.password) and not check_password(body[hard_fields[2]], user.password):
		user.password = parsers[hard_fields[2]](body[hard_fields[2]])
	user.save()
	return JsonResponse({'success': http.HTTPStatus(200).phrase}, status=200)
