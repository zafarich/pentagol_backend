from django.urls import include, path
from rest_framework.routers import SimpleRouter

from matches.views import MatchModelViewSet

router = SimpleRouter()
router.register('', MatchModelViewSet, 'matches')

urlpatterns = [
    path('', include(router.urls)),
]
