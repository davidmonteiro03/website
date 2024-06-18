from django.shortcuts import render
from django.http import JsonResponse
from django.template import loader
from django.forms.models import model_to_dict
from backend.models import Session, ApiLink
import json, http
from django.conf import settings

# Create your views here.
def model_to_json(model):
	target_dict = model_to_dict(model)
	result = {}
	for key in target_dict.keys():
		result[key] = target_dict[key]
	if 'id' in result:
		del result['id']
	if 'password' in result:
		del result['password']
	return result

def main(request):
	token = request.COOKIES.get('token')
	session = Session.objects.select_related('user').filter(session_token=token).first()
	json_data = {}
	if token and session:
		json_data['userdata'] = model_to_json(session.user)
		json_data['api_links'] = [model_to_json(link) for link in ApiLink.objects.all()]
		if not json_data['api_links']:
			del json_data['api_links']
		json_data['MEDIA_URL'] = settings.MEDIA_URL
	if request.method != 'POST':
		return render(request, 'main.html', context=json_data)
	if request.body == None or request.body == b'':
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400)
	body = json.loads(request.body)
	fields = ['type', 'file', 'data']
	if set(fields) != set(body.keys()):
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400)
	valid_types = ['navbar', 'app', 'modal', 'footer']
	if body['type'] not in valid_types:
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400)
	if not body['file']:
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400)
	json_data['api_data'] = {}
	json_data['api_data'][body['file'].split('.')[0]] = body['data']
	try:
		html = loader.render_to_string(body['file'], context=json_data)
		return JsonResponse({'success': http.HTTPStatus(200).phrase, 'html': html}, status=200)
	except:
		return JsonResponse({'error': http.HTTPStatus(404).phrase}, status=404)
