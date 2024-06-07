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
		return JsonResponse(None, safe=False, status=400)
	body = json.loads(request.body)
	fields = ['type', 'file', 'data']
	if set(fields) != set(body.keys()):
		return JsonResponse(None, safe=False, status=400)
	valid_types = ['navbar', 'app', 'modal', 'footer']
	if body['type'] not in valid_types:
		return JsonResponse(None, safe=False, status=400)
	if not body['file']:
		return JsonResponse(None, safe=False, status=400)
	data = body['data'] if 'data' in body.keys() else {}
	html = {'html': loader.render_to_string(body["file"], data)}
	return JsonResponse(html)
