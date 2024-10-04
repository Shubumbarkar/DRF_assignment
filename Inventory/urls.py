# main urls.py (project level)

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('inventory_app.urls')),  # Adjust to your app name
]
