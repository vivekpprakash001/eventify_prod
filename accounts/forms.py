from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'role',
                  'is_staff', 'is_customer', 'is_user')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-sm'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'role': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_customer': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_user': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Apply bootstrap small styling to password fields
        self.fields['password1'].widget.attrs.update({'class': 'form-control form-control-sm'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control form-control-sm'})


class LoginForm(AuthenticationForm):
    pass
