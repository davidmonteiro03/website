from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def signup(request):
	json_data = json.loads(request.body)
	print("ola")
	return JsonResponse(json_data)
