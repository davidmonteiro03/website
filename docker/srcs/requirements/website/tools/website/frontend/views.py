from django.shortcuts import render
from django.http import JsonResponse
from django.template import loader
import json
# from . import parse

# Create your views here.
def main(request):
	if request.method != 'POST':
		return render(request, 'main.html')
	if (request.body == None or request.body == b''):
		return JsonResponse({'error': 'Empty body'})
	body = json.loads(request.body)
	if 'type' not in body.keys():
		return JsonResponse({'error': 'No type'})
	valid_types = ['navbar', 'app', 'modal', 'footer']
	if body['type'] not in valid_types:
		return JsonResponse({'error': 'Invalid type'})
	if not body['file']:
		return JsonResponse({'error': 'No file'})
	data = body['data'] if 'data' in body.keys() else {}
	# print(data['file'])
	html = {'html': loader.render_to_string(body["file"], data)}
	# print(data)
	# print(html)
	return JsonResponse(html)
