from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.models import Category, Ads, Selection
from ads.permissions import AdsUpdatePermission, IsOwnerIsStaff
from ads.serializers import AdsListSerializer, AdsRetrieveSerializer, AdsCreateSerializer, AdsUpdateSerializer, \
    AdsDestroySerializer, CategorySerializer, SelectionListSerializer, SelectionDetailSerializer, \
    SelectionCreateSerializer


def start_page(request):
    return JsonResponse({'status': 'OK'}, status=200)


class CategoryListView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class AdsListView(ListAPIView):
    queryset = Ads.objects.order_by('-price').all()
    serializer_class = AdsListSerializer

    def get(self, request, *args, **kwargs):
        categories = request.GET.getlist('cat', [])
        if categories:
            self.queryset = self.queryset.filter(category_id__in=categories)
        text = request.GET.get('text')
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)
        location = request.GET.get('loc')
        if location:
            self.queryset = self.queryset.filter(author__location__name__icontains=location)
        price_from = request.GET.get('price_from')
        price_to = request.GET.get('price_to')
        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)
        if price_to:
            self.queryset = self.queryset.filter(price__lte=price_to)
        return super().get(self, *args, **kwargs)


class AdsDetailView(RetrieveAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsRetrieveSerializer
    permission_classes = [IsAuthenticated]


class AdsCreateView(CreateAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsCreateSerializer


class AdsUpdateView(UpdateAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsUpdateSerializer
    permission_classes = [AdsUpdatePermission]


class AdsDeleteView(DestroyAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsDestroySerializer


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
            "author": self.object.author.username,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "image": self.object.image.url if self.object.image else None
        })


class SelectionListView(ListAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionListSerializer


class SelectionDetailView(RetrieveAPIView):
    queryset = Selection
    serializer_class = SelectionDetailSerializer


class SelectionUpdateView(UpdateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionCreateSerializer
    permission_classes = [IsAuthenticated, IsOwnerIsStaff]


class SelectionCreateView(CreateAPIView):
    queryset = Selection
    serializer_class = SelectionCreateSerializer
    permission_classes = [IsAuthenticated]


class SelectionDeleteView(DestroyAPIView):
    queryset = Selection
    serializer_class = SelectionCreateSerializer
    permission_classes = [IsAuthenticated]
