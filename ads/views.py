import json

from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from Avito import settings
from ads.models import Category, Ads
from users.models import User


def start_page(request):
    return JsonResponse({'status': 'OK'}, status=200)


class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by('name')


        response = []
        for cat in self.object_list:
            response.append({
                'id': cat.id,
                'name': cat.name
            })
        return JsonResponse(response, safe=False)


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        cat = self.get_object()

        return JsonResponse({
            'id': cat.id,
            'name': cat.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)

        category = Category.objects.create(name=category_data['name'])
        return JsonResponse({
            'id': category.id,
            'name': category.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        category_data = json.loads(request.body)

        self.object.name = category_data['name']

        self.object.save()
        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


class AdsListView(ListView):
    model = Ads

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by('-price')

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        ads = []
        for ad in page_obj:
            ads.append({
                "id": ad.id,
                "name": ad.name,
                "author_id": ad.author_id,
                "price": ad.price,
                "image": ad.image.url if ad.image else None
            })

        response = {
            "items": ads,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }
        return JsonResponse(response, safe=False)


class AdsDetailView(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        ads = self.get_object()

        return JsonResponse({
            'id': ads.id,
            'name': ads.name,
            'author_id': ads.author_id,
            'price': ads.price,
            'description': ads.description,
            'is_published': ads.is_published,
            'image': ads.image.url if ads.image else None,
            'category_id': ads.category_id
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdsCreateView(CreateView):
    model = Ads
    fields = ['name', 'author_id', 'price', 'description', 'is_published', 'image', 'category_id']

    def post(self, request, *args, **kwargs):
        ads_data = json.loads(request.body)

        ads = Ads.objects.create(
            name=ads_data['name'],
            author_id=ads_data['author_id'],
            price=ads_data['price'],
            description=ads_data['description'],
            category_id=ads_data['category_id'],
        )

        return JsonResponse(
            {
                'id': ads.id,
                'name': ads.name,
                'author_id': ads.author_id,
                'price': ads.price,
                'description': ads.description,
                'is_published': ads.is_published,
                'category_id': ads.category_id,
                'image': ads.image.url if ads.image else None,

            }
        )


@method_decorator(csrf_exempt, name='dispatch')
class AdsUpdateView(UpdateView):
    model = Ads
    fields = ['name', 'author', 'price', 'description', 'is_published', 'image', 'category']

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ads_data = json.loads(request.body)

        self.object.name = ads_data['name']
        self.object.author_id = ads_data['author_id']
        self.object.price = ads_data['price']
        self.object.description = ads_data['description']
        self.object.category_id = ads_data['category_id']

        self.object.save()
        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
            'author_id': self.object.author_id,
            'price': self.object.price,
            'description': self.object.description,
            'is_published': self.object.is_published,
            'category_id': self.object.category_id,
            'image': self.object.image.url if self.object.image else None,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdsDeleteView(DeleteView):
    model = Ads
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdsImageView(UpdateView):
    model = Ads
    fields = ['name', 'author', 'price', 'description', 'is_published', 'image', 'category']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES['image']
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            #"author": self.object.author,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "image": self.object.image.url if self.object.image else None
        })


class UserAdsDetailView(View):
    def get(self, request):
        user_qs = Ads.objects.annotate(total_ads=Count('is_published'))

        by_user = User.objects.all()
        paginator = Paginator(by_user, settings.TOTAL_ON_PAGE_USER)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        users = []
        for user in page_obj:
            users.append(
                {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role,
                    "age": user.age,
                    #"location": "Москва",  # поле name из location
                    "total_ads": user_qs
                })
        response = {
            "items": users,
            "total": paginator.count,
            "num_page": paginator.num_pages
        }

        return JsonResponse(response, safe=False)
