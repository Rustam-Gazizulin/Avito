import json

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from ads.models import Category, Ads


def start_page(request):
    return JsonResponse({'status': 'OK'}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryView(View):
    def get(self, request):
        categories = Category.objects.all()

        response = []
        for cat in categories:
            response.append({
                'id': cat.id,
                'name': cat.name
            })
        return JsonResponse(response, safe=False)
    
    def post(self, request):
        category_data = json.loads(request.body)

        category = Category()
        category.name = category_data['name']

        category.save()
        return JsonResponse(
            {
                'id': category.id,
                'name': category.name,
            }
        )


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        cat = self.get_object()

        return JsonResponse({
            'id': cat.id,
            'name': cat.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdsView(View):
    def get(self, request):
        ads = Ads.objects.all()

        response = []
        for ad in ads:
            response.append({
                "id": ad.id,
                "name": ad.name,
                "author": ad.author,
                "price": ad.price
            })
        return JsonResponse(response, safe=False)
    
    def post(self, request):
        ads_data = json.loads(request.body)

        ads = Ads()
        ads.name = ads_data['name']
        ads.author = ads_data['author']
        ads.price = ads_data['price']
        ads.description = ads_data['description']
        ads.address = ads_data['address']
        ads.is_published = ads_data['is_published']

        ads.save()
        return JsonResponse(
            {
                'id': ads.id,
                'name': ads.name,
                'author': ads.author,
                'price': ads.price,
                'description': ads.description,
                'address': ads.address,
                'is_published': ads.is_published
            }
        )


class AdsDetailView(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        ads = self.get_object()

        return JsonResponse({
                "id": ads.id,
                "name": ads.name,
                "author": ads.author,
                "price": ads.price
            })
