
import requests
import json
from django.conf import settings
from django.http import JsonResponse

# This is a middleware to validate tokens. Some endpoints will need to use it
class JWTValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token_string = request.headers.get('Authorization')
        if token_string and token_string.startswith('Bearer '):
            try:
                response = requests.post(
                    f"{settings.BASE_URL}/auth/validate_token",
                    json={"token": token_string.split(' ')[1]}
                )
                
                if response.status_code == 200:
                    request.user_info = response.json()
                else:
                    return JsonResponse({"error": "Invalid or expired token"}, status=response.status_code)

            except requests.RequestException as e:
                return JsonResponse({"error": str(e)}, status=500)

        return self.get_response(request)
