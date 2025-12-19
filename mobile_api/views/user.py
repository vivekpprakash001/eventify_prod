# accounts/views.py
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.authtoken.models import Token
from mobile_api.forms import RegisterForm, LoginForm, WebRegisterForm
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import logout
from mobile_api.utils import validate_token_and_get_user
from utils.errors_json_convertor import simplify_form_errors
from accounts.models import User


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            form = RegisterForm(data)
            if form.is_valid():
                user = form.save()
                token, _ = Token.objects.get_or_create(user=user)
                return JsonResponse({'message': 'User registered successfully', 'token': token.key}, status=201)
            return JsonResponse({'errors': form.errors}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class WebRegisterView(View):
    def post(self, request):
        print('0')
        print('*' * 100)
        print(request.body)
        print('*' * 100)
        try:
            data = json.loads(request.body)
            form = WebRegisterForm(data)
            print('1')
            print('*' * 100)
            print(form.errors)
            print('*' * 100)
            if form.is_valid():
                print('2')
                user = form.save()
                token, _ = Token.objects.get_or_create(user=user)
                print('3')
                response = {
                    'message': 'User registered successfully',
                    'token': token.key,
                    'username': user.username,
                    'email': user.email,
                    'phone_number': user.phone_number,
                }
                return JsonResponse(response, status=201)
            return JsonResponse({'errors': form.errors}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request):
        print('0')
        try:
            data = json.loads(request.body)
            form = LoginForm(data)
            print('1')
            if form.is_valid(): 
                print('2')
                user = form.cleaned_data['user']
                token, _ = Token.objects.get_or_create(user=user)
                print('3')
                response = {
                    'message': 'Login successful', 
                    'token': token.key,
                    'username': user.username,
                    'email': user.email,
                    'phone_number': user.phone_number,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': user.role,
                    'pincode': user.pincode,
                    'district': user.district,
                    'state': user.state,
                    'country': user.country,
                    'place': user.place,
                    'latitude': user.latitude,
                    'longitude': user.longitude,
                    'profile_photo': request.build_absolute_uri(user.profile_picture.url) if user.profile_picture else ''
                }
                print('4')
                print(response)
                return JsonResponse(response, status=200)
            
            return JsonResponse(simplify_form_errors(form), status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class StatusView(View):
    def post(self, request):
        try:
            user, token, data, error_response = validate_token_and_get_user(request, error_status_code=True)
            if error_response:
                return error_response

            return JsonResponse({
                "status": "logged_in",
                "username": user.username,
                "email": user.email
            })

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(View):
    def post(self, request):
        try:
            user, token, data, error_response = validate_token_and_get_user(request, error_status_code=True)
            if error_response:
                return error_response

            # 🔍 Call Django's built-in logout
            logout(request)

            # 🗑 Delete the token to invalidate future access
            token.delete()

            return JsonResponse({
                "status": "logged_out",
                "message": "Logout successful"
            })

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class UpdateProfileView(View):
    def post(self, request):
        try:
            # Authenticate user using validate_token_and_get_user
            user, token, data, error_response = validate_token_and_get_user(request, error_status_code=True)
            if error_response:
                # Convert error response format to match our API response format
                error_data = json.loads(error_response.content)
                return JsonResponse({
                    'success': False,
                    'error': error_data.get('message', error_data.get('status', 'Authentication failed'))
                }, status=error_response.status_code)
            
            errors = {}
            updated_fields = []
            
            # Get update data - handle both JSON and multipart/form-data
            is_multipart = request.content_type and 'multipart/form-data' in request.content_type
            if is_multipart:
                # For multipart, get data from POST (data already contains token/username from validation)
                json_data = request.POST.dict()
            else:
                # For JSON, use data from validate_token_and_get_user
                json_data = data if data else {}

            # Update first_name
            if 'first_name' in json_data:
                first_name = json_data.get('first_name', '').strip()
                if first_name:
                    user.first_name = first_name
                    updated_fields.append('first_name')
                elif first_name == '':
                    user.first_name = ''
                    updated_fields.append('first_name')

            # Update last_name
            if 'last_name' in json_data:
                last_name = json_data.get('last_name', '').strip()
                if last_name:
                    user.last_name = last_name
                    updated_fields.append('last_name')
                elif last_name == '':
                    user.last_name = ''
                    updated_fields.append('last_name')

            # Update phone_number
            if 'phone_number' in json_data:
                phone_number = json_data.get('phone_number', '').strip()
                if phone_number:
                    # Check if phone number is already taken by another user
                    if User.objects.filter(phone_number=phone_number).exclude(id=user.id).exists():
                        errors['phone_number'] = 'Phone number is already registered.'
                    else:
                        user.phone_number = phone_number
                        updated_fields.append('phone_number')
                elif phone_number == '':
                    user.phone_number = None
                    updated_fields.append('phone_number')

            # Update email
            if 'email' in json_data:
                email = json_data.get('email', '').strip().lower()
                if email:
                    # Validate email format
                    if '@' not in email:
                        errors['email'] = 'Invalid email format.'
                    # Check if email is already taken by another user
                    elif User.objects.filter(email=email).exclude(id=user.id).exists():
                        errors['email'] = 'Email is already registered.'
                    else:
                        user.email = email
                        # Also update username if it was set to email
                        if user.username == user.email or not user.username:
                            user.username = email
                        updated_fields.append('email')
                elif email == '':
                    errors['email'] = 'Email cannot be empty.'

            # Update pincode
            if 'pincode' in json_data:
                pincode = json_data.get('pincode', '').strip()
                if pincode:
                    user.pincode = pincode
                    updated_fields.append('pincode')
                elif pincode == '':
                    user.pincode = None
                    updated_fields.append('pincode')

            # Update district
            if 'district' in json_data:
                district = json_data.get('district', '').strip()
                if district:
                    user.district = district
                    updated_fields.append('district')
                elif district == '':
                    user.district = None
                    updated_fields.append('district')

            # Update state
            if 'state' in json_data:
                state = json_data.get('state', '').strip()
                if state:
                    user.state = state
                    updated_fields.append('state')
                elif state == '':
                    user.state = None
                    updated_fields.append('state')

            # Update country
            if 'country' in json_data:
                country = json_data.get('country', '').strip()
                if country:
                    user.country = country
                    updated_fields.append('country')
                elif country == '':
                    user.country = None
                    updated_fields.append('country')

            # Update place
            if 'place' in json_data:
                place = json_data.get('place', '').strip()
                if place:
                    user.place = place
                    updated_fields.append('place')
                elif place == '':
                    user.place = None
                    updated_fields.append('place')

            # Handle profile_picture (multipart form-data only)
            if 'profile_photo' in request.FILES:
                # Handle file upload from multipart/form-data
                profile_photo = request.FILES['profile_photo']
                # Validate file type
                if not profile_photo.content_type.startswith('image/'):
                    errors['profile_photo'] = 'File must be an image.'
                else:
                    user.profile_picture = profile_photo
                    updated_fields.append('profile_photo')

            # Return errors if any
            if errors:
                return JsonResponse({
                    'success': False,
                    'errors': errors
                }, status=400)

            # Save user if any fields were updated
            if updated_fields:
                user.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Profile updated successfully',
                    'updated_fields': updated_fields,
                    'user': {
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'phone_number': user.phone_number,
                        'pincode': user.pincode,
                        'district': user.district,
                        'state': user.state,
                        'country': user.country,
                        'place': user.place,
                        'profile_picture': user.profile_picture.url if user.profile_picture else None,
                    }
                }, status=200)
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'No fields provided for update'
                }, status=400)

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
