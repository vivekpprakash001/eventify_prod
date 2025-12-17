from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=150, required=False, label="Full name")
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ("username", "full_name", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user = User
        if user.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        # Save full name to first_name/last_name if possible
        full_name = self.cleaned_data.get("full_name", "").strip()
        if full_name:
            parts = full_name.split(None, 1)
            user.first_name = parts[0]
            if len(parts) > 1:
                user.last_name = parts[1]
        user.email = self.cleaned_data["email"]
        user.is_active = True  # create inactive until email verified
        if commit:
            user.save()
        return user


class CustomerLoginForm(AuthenticationForm):
    """
    Wrapper around Django's AuthenticationForm to customize widgets.
    """
    username = forms.CharField(
        label="Email or Username",
        widget=forms.TextInput(attrs={
            "autofocus": True,
            "placeholder": "Email or username",
            "class": "input",
            "autocomplete": "username",
        })
    )

    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter your password",
            "class": "input",
            "autocomplete": "current-password",
        })
    )


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "pincode",
            "district",
            "state",
            "country",
            "place",
            "latitude",
            "longitude",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "pincode": forms.TextInput(attrs={"class": "form-control"}),
            "district": forms.TextInput(attrs={"class": "form-control"}),
            "state": forms.TextInput(attrs={"class": "form-control"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
            "place": forms.TextInput(attrs={"class": "form-control"}),
            "latitude": forms.NumberInput(attrs={"class": "form-control", "step": "any"}),
            "longitude": forms.NumberInput(attrs={"class": "form-control", "step": "any"}),
        }