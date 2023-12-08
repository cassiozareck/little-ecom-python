# views.py

from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from .models import Item
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

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
