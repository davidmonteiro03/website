# import Django modules
from django.urls import path # Path

# import views
from . import views

# urlpatterns
urlpatterns = [
	path('', views.main, name='main'), # Main
	path('server-data/', views.server_data, name='server_data'), # Components
]
