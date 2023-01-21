import json

from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from users.models import Location, User


class LocationListView(ListView):
    model = Location

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        response = []
        for loc in self.object_list:
            response.append({
                'id': loc.id,
                'name': loc.name
            })
        return JsonResponse(response, safe=False)


class LocationDetailView(DetailView):
    model = Location

    def get(self, request, *args, **kwargs):
        loc = self.get_object()

        return JsonResponse({
            'id': loc.id,
            'name': loc.name,
            'lat': loc.lat,
            'lng': loc.lng,
        })


@method_decorator(csrf_exempt, name='dispatch')
class LocationCreateView(CreateView):
    model = Location
    fields = ['name', 'lat', 'lng']

    def post(self, request, *args, **kwargs):
        location_data = json.loads(request.body)

        location = Location.objects.create(
            name=location_data['name'],
            lat=location_data['lat'],
            lng=location_data['lng']
        )
        return JsonResponse({
            'id': location.id,
            'name': location.name,
            'lat': location.lat,
            'lng': location.lng,
        })


@method_decorator(csrf_exempt, name='dispatch')
class LocationUpdateView(UpdateView):
    model = Location
    fields = ['name', 'lat', 'lng']

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        location_data = json.loads(request.body)

        self.object.name = location_data['name']
        self.object.lat = location_data['lat']
        self.object.lng = location_data['lng']

        self.object.save()
        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
            'lat': self.object.lat,
            'lng': self.object.lng
        })


@method_decorator(csrf_exempt, name='dispatch')
class LocationDeleteView(DeleteView):
    model = Location
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by('username')


        response = []
        for user in self.object_list:
            response.append({
                'id': user.id,
                'username': user.username,
                'last_name': user.last_name,
                'first_name': user.first_name,
                'role': user.role,
                'age': user.age,
                'location': list(map(str, user.location.all())),
            })
        return JsonResponse(response, safe=False)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        user = self.get_object()

        return JsonResponse({
            'id': user.id,
            'username': user.username,
            'last_name': user.last_name,
            'first_name': user.first_name,
            'role': user.role,
            'age': user.age,
            'location': list(map(str, user.location.all())),
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ['username', 'last_name', 'first_name', 'role', 'age', 'location']

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        user = User.objects.create(
            username=user_data['username'],
            last_name=user_data['last_name'],
            first_name=user_data['first_name'],
            role=user_data['role'],
            age=user_data['age'],
            )

        for loc in user_data['location']:
            loc_obj, created = Location.objects.get_or_create(
                name=loc,
                defaults={
                    'lat': 11.111111,
                    'lng': 22.222222,
                })
            user.location.add(loc_obj)
        user.save()

        return JsonResponse({
            'id': user.id,
            'username': user.username,
            'last_name': user.last_name,
            'first_name': user.first_name,
            'role': user.role,
            'age': user.age,
            'location': list(map(str, user.location.all())),
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'last_name', 'first_name', 'role', 'age', 'location']

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user_data = json.loads(request.body)

        self.object.username = user_data['username']
        self.object.last_name = user_data['last_name']
        self.object.first_name = user_data['first_name']
        self.object.role = user_data['role']
        self.object.age = user_data['age']

        for loc in user_data['location']:
            loc_obj, _ = Location.objects.get_or_create(name=loc,
                                                        defaults={
                                                            'lat': 11.111111,
                                                            'lng': 22.222222,
                                                        })
            self.object.location.add(loc_obj)

        self.object.save()
        return JsonResponse({
            'id': self.object.id,
            'username': self.object.username,
            'last_name': self.object.last_name,
            'first_name': self.object.first_name,
            'role': self.object.role,
            'age': self.object.age,
            'location': list(self.object.location.all().values_list('name', flat=True)),
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)



