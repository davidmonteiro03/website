from django.urls import path
from . import views

urlpatterns = [
	path('signup/', views.signup, name='signup'),
	path('signin/', views.signin, name='signin'),
	path('signout/', views.signout, name='signout'),
	path('getuser/', views.getuser, name='getuser'),
	path('update/', views.update, name='update'),
]
