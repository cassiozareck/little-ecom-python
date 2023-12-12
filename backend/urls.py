# urls.py

from django.urls import path
from .views import remove_item, add_item, get_items, update_item, buy_item  # Import the view

urlpatterns = [
    
    path('remove-item/<int:item_id>/', remove_item, name='remove_item'),
    path('add-item/', add_item, name='add_item'),
    path('items/', get_items, name='get_items'),
    path('update/', update_item, name='update_item'),
    path('buy-item', buy_item, name="buy_item"),
]
