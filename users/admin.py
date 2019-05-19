from django.contrib import admin
# from rest_framework.authtoken.models import Token
# from django.contrib import admin

# admin.site.unregister(Token)
# Register your models here.
from .models import Profile
from django.contrib.auth.models import User, Group


admin.site.register(Profile)
