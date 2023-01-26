import json

from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from ads.models import Ads
from users.models import Location, User
from users.serializers import UserListSerializer, UserDetailSerializer, UserCreateSerializer, UserUpdateSerializer, \
    UserDestroySerializer, LocationSerializer


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class =LocationSerializer


#     def get(self, request, *args, **kwargs):
#         super().get(request, *args, **kwargs)
#
#         response = []
#         for loc in self.object_list:
#             response.append({
#                 'id': loc.id,
#                 'name': loc.name
#             })
#         return JsonResponse(response, safe=False)
#
#
# class LocationDetailView(DetailView):
#     model = Location
#
#     def get(self, request, *args, **kwargs):
#         loc = self.get_object()
#
#         return JsonResponse({
#             'id': loc.id,
#             'name': loc.name,
#             'lat': loc.lat,
#             'lng': loc.lng,
#         })
#
#
# @method_decorator(csrf_exempt, name='dispatch')
# class LocationCreateView(CreateView):
#     model = Location
#     fields = ['name', 'lat', 'lng']
#
#     def post(self, request, *args, **kwargs):
#         location_data = json.loads(request.body)
#
#         location = Location.objects.create(
#             name=location_data['name'],
#             lat=location_data['lat'],
#             lng=location_data['lng']
#         )
#         return JsonResponse({
#             'id': location.id,
#             'name': location.name,
#             'lat': location.lat,
#             'lng': location.lng,
#         })
#
#
# @method_decorator(csrf_exempt, name='dispatch')
# class LocationUpdateView(UpdateView):
#     model = Location
#     fields = ['name', 'lat', 'lng']
#
#     def post(self, request, *args, **kwargs):
#         super().post(request, *args, **kwargs)
#
#         location_data = json.loads(request.body)
#
#         self.object.name = location_data['name']
#         self.object.lat = location_data['lat']
#         self.object.lng = location_data['lng']
#
#         self.object.save()
#         return JsonResponse({
#             'id': self.object.id,
#             'name': self.object.name,
#             'lat': self.object.lat,
#             'lng': self.object.lng
#         })
#
#
# @method_decorator(csrf_exempt, name='dispatch')
# class LocationDeleteView(DeleteView):
#     model = Location
#     success_url = '/'
#
#     def delete(self, request, *args, **kwargs):
#         super().delete(request, *args, **kwargs)
#
#         return JsonResponse({"status": "ok"}, status=200)


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDestroySerializer



