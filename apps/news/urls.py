from django.urls import include, path
from rest_framework.routers import SimpleRouter

from matches.views import MatchModelViewSet
from news.views import CategoryNewsModelViewSet, NewsModelViewSet

router = SimpleRouter()
router.register('categories', CategoryNewsModelViewSet, 'categories')
router.register('', NewsModelViewSet, 'news')

urlpatterns = [
    path('', include(router.urls)),
]
