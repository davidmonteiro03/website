from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

# Create your views here.
def main(request):
    return render(request, 'main.html')

def index(request):
    html = render_to_string('index.html')
    return JsonResponse({'html': html})
