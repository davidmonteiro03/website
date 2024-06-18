from django.urls import path
from . import views

urlpatterns = [
	path('ligaportugal/', views.ligaportugal, name='ligaportugal'),
]
