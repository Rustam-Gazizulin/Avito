from rest_framework import serializers

from ads.models import Ads, Category, Selection
from users.models import User


class AdsListSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField()
    author = serializers.CharField()
    category = serializers.CharField()

    class Meta:
        model = Ads
        fields = ['id', 'name', 'author_id', 'author', 'category', 'price', 'image']


class AdsRetrieveSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField()
    author = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    category = serializers.CharField()

    class Meta:
        model = Ads
        fields = ['id', 'name', 'author_id', 'author', 'category', 'price', 'image']


class AdsCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    class Meta:
        model = Ads
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        ads = Ads.objects.create(**validated_data)
        ads.save()
        return ads


class AdsUpdateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    is_published = serializers.BooleanField(required=False)

    class Meta:
        model = Ads
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        ads = super().save()

        return ads


class AdsDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        field = ['id']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SelectionListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Selection
        fields = ['id', 'name']


class SelectionDetailSerializer(serializers.ModelSerializer):
    items = AdsListSerializer(many=True)

    class Meta:
        model = Selection
        fields = '__all__'


class SelectionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Selection
        fields = '__all__'
