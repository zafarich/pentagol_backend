from django.urls import include, path
from rest_framework.routers import SimpleRouter

from championship.views import ChampionshipModelViewSet, SeasonModelViewSet

router = SimpleRouter()
router.register('season', SeasonModelViewSet, 'seasons')
router.register('', ChampionshipModelViewSet, 'championships')

urlpatterns = [
    path('', include(router.urls)),
]
