# import Django modules
from django.urls import path # Django path

# import views
from . import views

# urlpatterns
urlpatterns = [
	path('', views.main, name='main'), # Main
]
