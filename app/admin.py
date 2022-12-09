from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import User

class MyUserAdmin(UserAdmin):
    pass

admin.site.register(User, MyUserAdmin)