from django.contrib import admin

# Register your models here.
from .models import User, Session

admin.site.register(User)
admin.site.register(Session)
