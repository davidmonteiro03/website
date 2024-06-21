# import Python modules
import json # JSON encoder and decoder
import http # HTTP status codes
import os # Miscellaneous operating system interfaces

# import Django modules
from django.http import JsonResponse # JSON response
from django.template import loader # Load a template
from django.views.decorators.http import require_POST # Require POST method
from django.conf import settings # Django settings

# Function to render template
# :param request: HTTP request
# :return: HTTP response
@require_POST # Require POST method
def main(request):
	template_path = os.path.join(settings.BASE_DIR, 'api', 'templates') # Get template path from settings
	json_data = {} # Initialize JSON data
	if request.body == None or request.body == b'': # Check if request body is empty
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400) # Return error response
	body = json.loads(request.body) # Load JSON data from request body
	fields = ['type', 'file'] # Initialize fields
	if set(fields) != set(body.keys()): # Check if fields are not in body
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400) # Return error response
	valid_types = ['navbar', 'content', 'modal', 'footer'] # Initialize valid types
	if body['type'] not in valid_types: # Check if type is not in valid types
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400) # Return error response
	if not body['file']: # Check if file is empty
		return JsonResponse({'error': http.HTTPStatus(400).phrase}, status=400) # Return error response
	try: # Try to render template
		html = loader.render_to_string(os.path.join(template_path, f'{body["file"]}.html'), context=json_data)
		return JsonResponse({ # Return JSON response
			'success': http.HTTPStatus(200).phrase, # Success message
			'html': html # HTML data
		}, status=200) # Return success response
	except: # Catch exceptions
		return JsonResponse({'error': http.HTTPStatus(404).phrase}, status=404) # Return error response
