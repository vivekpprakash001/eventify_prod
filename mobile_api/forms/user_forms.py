# accounts/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Ensure both email and username do not clash, since we set username = email
        if User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
            raise forms.ValidationError("Email is already registered.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Phone number is already registered.")
        return phone_number

    def save(self, commit=True):
        user = super().save(commit=False)
        # Set username equal to email to avoid separate username errors
        user.username = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class WebRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password', 'confirm_password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Ensure both email and username do not clash, since we set username = email
        if User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
            raise forms.ValidationError("Email is already registered.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Phone number is already registered.")
        return phone_number

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Set username equal to email to avoid separate username errors
        user.username = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])
        print('*' * 100)
        print(user.username)
        print('*' * 100)
        if commit:
            user.save()
        return user



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        print('*' * 100)
        print(username, password)
        print('*' * 100)
        
        if not username or not password:
            raise forms.ValidationError("Username and password are required.")
        
        # Check if username contains '@' (email) or is a regular username
        try:
            if '@' in username:
                print('1 **********************')
                # Try to find user by email
                user = User.objects.get(email=username)
                print(user)
                print('2 **********************')
                username = user.username
                print('3 **********************')
            else:
                print('4 **********************')# Use username as-is
                user = User.objects.get(username=username)
        except User.DoesNotExist:
            print('5 **********************')
            raise forms.ValidationError("Invalid credentials.")
        
        # Authenticate with the resolved username
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid credentials.")
        
        cleaned_data['user'] = user
        return cleaned_data
