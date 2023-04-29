from django.urls import include, path
from rest_framework.routers import SimpleRouter

from extra.views import LanguageModelViewSet

router = SimpleRouter()
router.register('language', LanguageModelViewSet, 'languages')

urlpatterns = [
    path('', include(router.urls)),
]
