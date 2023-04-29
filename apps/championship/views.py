from rest_framework.viewsets import ModelViewSet

from championship.models import Championship, Season
from championship.serializers import ChampionshipSerializers, SeasonSerializers


class ChampionshipModelViewSet(ModelViewSet):
    queryset = Championship.objects.all()
    serializer_class = ChampionshipSerializers


class SeasonModelViewSet(ModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializers
