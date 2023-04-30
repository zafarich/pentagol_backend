from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from extra.views import ModelViewSetWithNumberPaginationViewSet
from news.models import News, CategoryNews
from news.serializers import NewsSerializers, NewsGetSerializers, CategoriesSerializers


class CategoryNewsModelViewSet(ModelViewSet):
    queryset = CategoryNews.objects.all()
    serializer_class = CategoriesSerializers
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filter_fields = ['category']


class NewsModelViewSet(ModelViewSetWithNumberPaginationViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializers

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return NewsGetSerializers
        return super().get_serializer_class()
