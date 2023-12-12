# views.py

from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from .models import Item
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from .models import Item

@csrf_exempt
@require_http_methods(["DELETE"])
def remove_item(request, item_id):

    # This is important to retrieve the user's email
    # using middleware
    user_info = getattr(request, 'user_info', None)
    if not user_info or 'email' not in user_info:
        return HttpResponseBadRequest("Unauthorized access")

    owner = user_info['email'].split('@')[0]

    try:
        item = get_object_or_404(Item, pk=item_id)
        if not item.is_owner(owner):
            return HttpResponseBadRequest("You must be the item's owner to delete it.")
        
        item.delete()
        return HttpResponse(status=204)

    except Item.DoesNotExist:
        return HttpResponseNotFound("Item not found")

@csrf_exempt
@require_http_methods(["POST"])
def add_item(request):
    try:
        data = json.loads(request.body)
       
        if not email:
            return HttpResponseBadRequest("Email is required")

        username = email.split('@')[0]

        # Create a new Item instance
        item = Item.objects.create(
            owner=username,
            name=data.get('name'),
            price=data.get('price')
        )

        item.clean()

        # Return the ID of the newly created item
        return JsonResponse({'id': item.id}, status=201)

    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")
    except KeyError:
        return HttpResponseBadRequest("Missing fields in JSON")


@csrf_exempt
@require_http_methods(["PATCH"])
def update_item(request, id):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    # Authenticate user
    user_info = getattr(request, 'user_info', None)
    if not user_info or 'email' not in user_info:
        return HttpResponseBadRequest("Unauthorized access")
    owner = user_info['email'].split('@')[0]

    # Check if the item exists and owner matches
    if not Item.objects.filter(id=id, owner=owner).exists():
        return HttpResponseNotFound("Item not found or unauthorized access")

    # Update the item if it exists
    Item.objects.filter(id=id).update(
        name=data.get('name', ''),
        price=data.get('price', 0)
    )

    return JsonResponse({'message': 'Item updated successfully'}, status=200)

@csrf_exempt
@require_http_methods(["GET"])
def get_items(request):
    try:
        items = Item.objects.all()
        items_data = [item.to_dict() for item in items]  # Ensure Item model has a to_dict method
        return JsonResponse({'items': items_data}, safe=False)
    except Exception as e:
        # Log the exception for debugging purposes
        # Use a logger in production code
        print(f"Error retrieving items: {e}")
        return HttpResponseServerError("Internal Server Error")


@csrf_exempt
@require_http_methods(["POST"])
def buy_item(request):
    try:
        # Parse JSON data from the request
        data = json.loads(request.body)
        item_id = data.get("id")

        # Authenticate user
        user_info = getattr(request, 'user_info', None)
        if not user_info or 'email' not in user_info:
            return HttpResponseBadRequest("Unauthorized access")
        buyer = user_info['email'].split('@')[0]

        # Retrieve the item
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return HttpResponseNotFound("Item not found")

        # Check if the buyer is not the owner of the item
        if item.owner == buyer:
            return HttpResponseBadRequest("Cannot buy your own item")

        Item.objects.delete(id=item_id)

        return JsonResponse({'message': 'Item bought successfully', 'item_id': str(item_id)}, status=200)

    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")
    except Exception as e:
        # Log the exception for debugging purposes
        # Use a logger in production code
        print(f"Error in buying item: {e}")
        return HttpResponseServerError("Internal Server Error")


        