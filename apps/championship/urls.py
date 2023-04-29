from django.urls import include, path
from rest_framework.routers import SimpleRouter

from championship.views import ChampionshipModelViewSet, SeasonModelViewSet

router = SimpleRouter()
router.register('', ChampionshipModelViewSet, 'championships')
router.register('season', SeasonModelViewSet, 'seasons')

urlpatterns = [
    path('', include(router.urls)),
]
