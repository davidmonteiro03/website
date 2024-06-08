from django.shortcuts import render
from django.http import JsonResponse
from django.template import loader
from django.views.decorators.http import require_POST
from backend.models import Users
import json, http

# Create your views here.
def main(request):
	token = request.COOKIES.get('token')
	target = Users.objects.filter(token=token).first()
	json_data = {}
	if token and target:
		json_data['token'] = token
		json_data['userdata'] = {
			'fname': target.fname,
			'lname': target.lname,
			'username': target.username,
			'email': target.email,
			'profilephoto': target.profilephoto
		}
	if request.method != 'POST':
		return render(request, 'main.html', json_data)
	if request.body == None or request.body == b'':
		return JsonResponse({'error': http.HTTPStatus(400)}, status=400)
	body = json.loads(request.body)
	fields = ['type', 'file']
	if set(fields) != set(body.keys()):
		return JsonResponse({'error': http.HTTPStatus(400)}, status=400)
	valid_types = ['navbar', 'app', 'modal', 'footer']
	if body['type'] not in valid_types:
		return JsonResponse({'error': http.HTTPStatus(400)}, status=400)
	if not body['file']:
		return JsonResponse({'error': http.HTTPStatus(400)}, status=400)
	html = loader.render_to_string(body['file'], json_data)
	return JsonResponse({'success': http.HTTPStatus(200), 'html': html}, status=200)
