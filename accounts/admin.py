from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Extra', {'fields':('phone_number','role','is_customer','is_user')}),
    )
    list_display = ('username','email','phone_number','role','is_staff')
