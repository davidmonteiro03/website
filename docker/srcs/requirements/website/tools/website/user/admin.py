# import Django modules
from django.contrib import admin # Django admin

# import models
from .models import User # User model
from .models import Session # Session model

# Register models
admin.site.register(User) # Register User model
admin.site.register(Session) # Register Session model
