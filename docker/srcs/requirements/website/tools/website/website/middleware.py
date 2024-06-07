import http
from django.http import HttpResponseServerError, HttpResponse
from django.template import loader

class CustomErrorHandlerMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		try:
			response = self.get_response(request)
			if response.status_code == 200:
				return response
			html = loader.render_to_string('error.html', context={
				'code': response.status_code,
				'message': http.HTTPStatus(response.status_code).phrase
			})
			return HttpResponse(html, status=response.status_code)
		except Exception as e:
			return HttpResponseServerError('Error occurred')
