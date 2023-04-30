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
    body_partial = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = [
            'id',
            'title',
            'body',
            'body_partial',
            'slug',
            'image',
            'category',
            'author',
            'created_at',
        ]

    def get_body_partial(self, obj):
        body = {}
        for key in obj.body.keys():
            body[key] = ' '.join(obj.body[key].split(' ')[:15])
        return body


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
