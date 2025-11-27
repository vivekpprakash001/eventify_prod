from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email','phone_number','role','is_staff','is_customer','is_user')

from django.contrib.auth.forms import AuthenticationForm
class LoginForm(AuthenticationForm):
    pass
