# urls.py

from django.urls import path
from .views import remove_item  # Import the view

urlpatterns = [
    
    path('remove-item/<int:item_id>/', remove_item, name='remove_item'),
    
]
