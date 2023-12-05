from django.shortcuts import render

# views.py
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import Account
import json

def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data['email']
            password = data['password']

            # Validate email
            validate_email(email)

            # Check if account already exists
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
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

