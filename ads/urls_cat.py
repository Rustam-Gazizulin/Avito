from django.urls import path, include
from rest_framework import routers

from ads.views import CategoryListView

router = routers.SimpleRouter()
router.register('', CategoryListView)

urlpatterns = [
    path('', include(router.urls))
    ]
