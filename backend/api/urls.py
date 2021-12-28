"""
    api/urls.py
    
    Define a set of URLs that map to REST API endpoints.
"""

from django.urls import include, path
from rest_framework import routers
from payments import api_views

# Intantiate Django REST Framework Router
# https://www.django-rest-framework.org/api-guide/routers/
router = routers.DefaultRouter()
# TODO: Register routers once we have viewsets

urlpatterns = [
    path('', include(router.urls))
]
