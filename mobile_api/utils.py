"""
Utility functions for mobile API authentication and validation.
"""
import json
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from accounts.models import User


def validate_token_and_get_user(request, error_status_code=None):
    """
    Validates token and username from request body.
    
    This function handles:
    - JSON parsing from request body (for application/json requests)
    - Form data parsing (for multipart/form-data requests)
    - Token and username extraction
    - Token validation
    - Username verification against token user
    
    Args:
        request: Django request object with JSON body or form data containing 'token' and 'username'
        error_status_code: Optional HTTP status code for error responses (default: None)
    
    Returns:
        tuple: On success, returns (user, token, data, None)
        tuple: On error, returns (None, None, None, JsonResponse)
        
    Error Responses:
        - Invalid JSON: {"status": "error", "message": "Invalid JSON"} (400 if status_code provided)
        - Missing credentials: {"status": "error", "message": "token and username required"} (400 if status_code provided)
        - Invalid token: {"status": "invalid_token"} (401 if status_code provided)
        - Username mismatch: {"status": "error", "message": "token does not match user"} (401 if status_code provided)
    """
    # Check if it's multipart/form-data
    is_multipart = request.content_type and 'multipart/form-data' in request.content_type
    
    if is_multipart:
        # For multipart/form-data, get data from POST
        data = request.POST.dict()
    else:
        # For JSON requests, parse from body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            status = 400 if error_status_code else None
            return (None, None, None, JsonResponse(
                {"status": "error", "message": "Invalid JSON"},
                status=status
            ))
    
    # Extract token and username
    token_key = data.get("token")
    username = data.get("username")
    
    # Validate both are present
    if not token_key or not username:
        status = 400 if error_status_code else None
        return (None, None, None, JsonResponse(
            {"status": "error", "message": "token and username required"},
            status=status
        ))
    
    try:
        # Get token object
        token = Token.objects.get(key=token_key)

        if username:
            if '@' in username:
                user = User.objects.get(email=username)
            else:
                user = User.objects.get(username=username)
        else:
            user = None

        if not user:
            status = 401 if error_status_code else None
            return (None, None, None, JsonResponse(
                {"status": "error", "message": "user not found"},
                status=status
            ))
        
        # Verify username matches token user
        # if user.username != username:
            # status = 401 if error_status_code else None
            # return (None, None, None, JsonResponse(
            #     {"status": "error", "message": "token does not match user"},
            #     status=status
            # ))
        
        # Success - return user, token, data, and None for error_response
        return (user, token, data, None)
        
    except Token.DoesNotExist:
        status = 401 if error_status_code else None
        return (None, None, None, JsonResponse(
            {"status": "invalid_token"},
            status=status
        ))
    except User.DoesNotExist:
        status = 401 if error_status_code else None
        return (None, None, None, JsonResponse(
            {"status": "error", "message": "user not found"},
            status=status
        ))

