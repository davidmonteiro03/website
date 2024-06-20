# import Python modules
import http # HTTP status codes
import json # JSON encoder and decoder
import requests # HTTP requests

# import Django modules
from django.views.decorators.http import require_GET # Require GET method
from django.http import JsonResponse # JSON response

# import parse
from . import parse # parse module

# import models
from .models import ApiLink # ApiLink model

# Function to get Liga Portugal standings
# :param request: HTTP request
# :return: JSON response
@require_GET # Require GET method
def ligaportugal(request):
	find_link = ApiLink.objects.filter(link='ligaportugal').first() # Find Liga Portugal link
	if not find_link: # Check if link does not exist
		return JsonResponse({'error': http.HTTPStatus(404).phrase}, status=404) # Return error response
	response = requests.get('https://www.ligaportugal.pt/pt/liga/standings/1') # Send GET request
	try: # Try to parse response
		in_data = json.loads(response.text) # Load JSON data from response
		out_data = parse.ligaportugal(in_data) # Parse Liga Portugal data
		if not out_data: # Check if data does not exist
			raise Exception # Raise exception
		return JsonResponse({ # Return JSON response
			'success': http.HTTPStatus(200).phrase, # Success message
			'content': out_data # Content data
		}, status=200) # Return success response
	except: # Catch exceptions
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400) # Return error response
