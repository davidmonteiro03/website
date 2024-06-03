from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

def change_page(request, page):
	if (request.method != 'POST'):
		return redirect(body)
	html = {'html': loader.render_to_string(f'{page}.html')}
	if request.body == None or request.body == b'':
		return JsonResponse(html)
	data = json.loads(request.body)
	html = {'html': loader.render_to_string(f'{page}.html', data)}
	return JsonResponse(html)

def body(request):
	return render(request, 'body.html')

@csrf_exempt
def navbar(request):
	return change_page(request, 'navbar')

@csrf_exempt
def modal(request):
	return change_page(request, 'modal')

@csrf_exempt
def index(request):
	return change_page(request, 'index')

@csrf_exempt
def profilepage(request):
	return change_page(request, 'profilepage')

def handler404(request, exception):
	return redirect(body)
