from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from ads import views

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api-auth/", include('rest_framework.urls')),

    path("", views.start_page, name='start'),

    path("cat/", include('ads.urls_cat')),

    path("ads/", include('ads.urls_ads')),

    path("sel/", include('ads.urls_sel')),

    path("loc/", include('users.urls_loc')),

    path("user/", include('users.urls_user'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
