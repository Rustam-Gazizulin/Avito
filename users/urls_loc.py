from django.urls import path, include
from rest_framework import routers

from users.views import LocationViewSet

router = routers.SimpleRouter()
router.register('', LocationViewSet)

urlpatterns = [
    path('', include(router.urls))
    ]
