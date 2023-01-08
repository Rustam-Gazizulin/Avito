from django.contrib import admin
from django.urls import path

from ads import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.start_page, name='start'),

    path("cat/", views.CategoryView.as_view(), name='category'),
    path('cat/<int:pk>/', views.CategoryDetailView.as_view()),

    path("ad/", views.AdsView.as_view(), name='ads'),
    path('ad/<int:pk>/', views.AdsDetailView.as_view()),

]
