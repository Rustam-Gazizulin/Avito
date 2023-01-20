from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from ads import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.start_page, name='start'),

    path("cat/", views.CategoryView.as_view(), name='category'),
    path('cat/<int:pk>/', views.CategoryDetailView.as_view()),


    path("ad/", views.AdsView.as_view(), name='ads'),
    path('ad/<int:pk>/', views.AdsDetailView.as_view()),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
