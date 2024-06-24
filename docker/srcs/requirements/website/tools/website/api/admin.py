# import Django modules
from django.contrib import admin # Django administration

# import models
from .models import ApiLink # ApiLink model

# Register models
admin.site.register(ApiLink) # Register ApiLink model
