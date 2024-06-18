from django.contrib import admin

# Register your models here.
from .models import User, Session, ApiLink

admin.site.register(User)
admin.site.register(Session)
admin.site.register(ApiLink)
