
from django.urls import path
from .views import (register,login,create_item,read_item,update_item,delete_item,
)

urlpatterns = [
    path('register/', register, name='register'),  
    path('login/', login, name='login'),  
    path('items/', create_item, name='create_item'),  
    path('items/<int:item_id>/', read_item, name='read_item'), 
    path('items/<int:item_id>/', update_item, name='update_item'), 
    path('items/<int:item_id>/', delete_item, name='delete_item'), 
]
