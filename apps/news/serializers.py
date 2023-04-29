from rest_framework import serializers

from news.models import News, CategoryNews


class CategoriesSerializers(serializers.ModelSerializer):
    class Meta:
        model = CategoryNews
        fields = [
            'id',
            'title',
        ]

        read_only_fields = [
            'id',
        ]


class NewsGetSerializers(serializers.ModelSerializer):
    category = CategoriesSerializers()

    class Meta:
        model = News
        fields = [
            'id',
            'title',
            'body',
            'slug',
            'image',
            'category',
            'author',
        ]


class NewsSerializers(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = [
            'id',
            'title',
            'body',
            'slug',
            'image',
            'category',
            'author',
        ]

        read_only_fields = [
            'id',
        ]

