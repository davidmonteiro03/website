import http, json, requests
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from . import parse

# Create your views here.
@require_POST
def ligaportugal(request):
	response = requests.get('https://www.ligaportugal.pt/pt/liga/standings/1')
	try:
		in_data = json.loads(response.text)
		out_data = parse.ligaportugal(in_data)
		if not out_data:
			raise Exception
		return JsonResponse({
			'success': http.HTTPStatus(200).phrase,
			'ligaportugal': out_data
		}, status=200)
	except:
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400)
