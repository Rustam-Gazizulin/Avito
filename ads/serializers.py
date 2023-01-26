from rest_framework import serializers

from ads.models import Ads


class AdsListSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField()
    author = serializers.CharField()
    category = serializers.CharField()

    class Meta:
        model = Ads
        fields = ['id', 'name', 'author_id', 'author', 'category', 'price', 'image']
