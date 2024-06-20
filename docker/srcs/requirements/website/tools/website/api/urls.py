# import Django modules
from django.urls import path # URL paths

# import views
from . import views

# urlpatterns
urlpatterns = [
	path('ligaportugal/', views.ligaportugal, name='ligaportugal'), # Liga Portugal
]
