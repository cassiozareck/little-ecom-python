from django.shortcuts import render

# views.py
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate
from .models import Account
import json
import jwt
import os

@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    try:
        data = json.loads(request.body)
        email = data['email']
        password = data['password']

        # Validate email
        validate_email(email)

        # Since we're using email as username we filter by email field 
        if Account.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Account already exists'}, status=400)
        
        # Validate password length
        if len(password) < 6:
            return JsonResponse({'error': 'Password must be at least 6 characters long'}, status=400)

        # Use AccountManager to create and save the user
        Account.objects.create_user(email=email, password=password)
        
        return JsonResponse({'message': 'User created successfully'}, status=201)
     
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'An error occurred'}, status=500)
    
@csrf_exempt
@require_http_methods(["POST"])
def sign_in(request):
    try:
        data = json.loads(request.body)
        email = data['email']
        password = data['password']

        validate_email(email)

    except (KeyError, json.JSONDecodeError, ValidationError):
        return JsonResponse({'error': 'Invalid data'}, status=400)

    # Authenticate search username and check the hash of password 
    # using some hashing algorithm
    user = authenticate(username=email, password=password)
    if user is None:
        return JsonResponse({'error': 'Invalid credentials'}, status=400)
    
    token = jwt.encode({
        'email': user.email,
        'exp': int((datetime.utcnow() + timedelta(days=30)).timestamp())
    }, os.getenv("JWT_KEY"), algorithm="HS256")

    return JsonResponse({'token': token}, status=200)