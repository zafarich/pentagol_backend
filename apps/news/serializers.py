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
    title = serializers.JSONField()

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
            'created_at',
        ]


class NewsSerializers(serializers.ModelSerializer):
    title = serializers.JSONField()

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
            'created_at',
        ]

        read_only_fields = [
            'id',
            'created_at',
        ]
