from django.urls import path
from . import views

urlpatterns = [
	path('', views.body, name='body'),
	path('navbar/', views.navbar, name='navbar'),
	path('modal/', views.modal, name='modal'),
	path('index/', views.index, name='index'),
	path('profilepage/', views.profilepage, name='profilepage'),
]

handler404 = views.handler404
