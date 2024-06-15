import http, os, json, requests
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from django.core.files.storage import default_storage
from . import parse
from .models import Users, Sessions
from frontend.views import model_to_json
from website import settings

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
	if Users.objects.filter(Q(username=parsing['username']) | Q(email=parsing['email'])).exists():
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
	if request.body == b'':
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

@require_POST
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
	target = Users.objects.filter(Q(username=body[field]) | Q(email=body[field])).first()
	if target:
		return JsonResponse({'error': http.HTTPStatus(401).phrase}, status=401)
	return JsonResponse({'success': http.HTTPStatus(200).phrase}, status=200)

@require_POST
def update(request):
	cookies = {}
	for key in request.COOKIES:
		cookies[key] = request.COOKIES[key]
	if 'token' not in cookies.keys():
		return JsonResponse({'error': http.HTTPStatus(401).phrase}, status=401)
	session = Sessions.objects.select_related('user').filter(session_token=cookies['token']).first()
	if not session:
		return JsonResponse({'error': http.HTTPStatus(401).phrase}, status=401)
	if request.body == b'':
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400)
	body = json.loads(request.body)
	soft_fields = ['fname', 'lname']
	hard_fields = ['username', 'oldpassword', 'newpassword']
	fields = soft_fields + hard_fields
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
		target = Users.objects.filter(username=parsers[hard_fields[0]](body[hard_fields[0]])).first()
		if not target:
			user.username = parsers[hard_fields[0]](body[hard_fields[0]])
			old_file_path = os.path.join('static/profilephotos', user.profilephoto)
			new_file_name = f"{user.username}{os.path.splitext(user.profilephoto)[1]}"
			new_file_path = os.path.join('static/profilephotos', new_file_name)
			if default_storage.exists(old_file_path):
				with default_storage.open(old_file_path) as old_file:
					default_storage.save(new_file_path, old_file)
				default_storage.delete(old_file_path)
				user.profilephoto = new_file_name
	if parsers[hard_fields[1]](body[hard_fields[1]]) and check_password(body[hard_fields[1]], user.password):
		user.password = parsers[hard_fields[2]](body[hard_fields[2]])
	user.save()
	return JsonResponse({'success': http.HTTPStatus(200).phrase}, status=200)
