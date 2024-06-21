# import Django modules
from django.urls import path # Django path

# import views
from . import views

# urlpatterns
urlpatterns = [
	path('', views.main, name='main'), # Main
	path('signup/', views.signup, name='signup'), # Sign Up
	path('signin/', views.signin, name='signin'), # Sign In
	path('signout/', views.signout, name='signout'), # Sign Out
	path('getuser/', views.getuser, name='getuser'), # Get User
	path('update/', views.update, name='update'), # Update
]
