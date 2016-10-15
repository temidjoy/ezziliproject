from django.contrib import admin
from rest_framework.authtoken.models import Token
from EzziliApp.models import UserCredentials, Adverts, Photo


admin.site.register(UserCredentials)
admin.site.register(Adverts)
admin.site.register(Photo)