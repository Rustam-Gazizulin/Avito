from django.urls import path

from users import views


urlpatterns = [
    path('', views.LocationListView.as_view(), name='location'),
    path('<int:pk>/', views.LocationDetailView.as_view()),
    path('create/', views.LocationCreateView.as_view()),
    path('update/<int:pk>/', views.LocationUpdateView.as_view()),
    path('delete/<int:pk>/', views.LocationDeleteView.as_view()),
    ]
