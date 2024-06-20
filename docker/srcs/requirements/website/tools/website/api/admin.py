# import Django modules
from django.contrib import admin # Django admin

# import models
from .models import ApiLink # ApiLink model

admin.site.register(ApiLink) # Register ApiLink model with Django admin
