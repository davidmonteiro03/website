from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django import db

@csrf_exempt
def signup(request):
	json_data = json.loads(request.body)
	return JsonResponse(json_data)
