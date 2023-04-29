from rest_framework.viewsets import ModelViewSet

from championship.models import Championship, Season
from championship.serializers import ChampionshipSerializers, SeasonCreateSerializers, SeasonGetSerializers


class ChampionshipModelViewSet(ModelViewSet):
    queryset = Championship.objects.all()
    serializer_class = ChampionshipSerializers


class SeasonModelViewSet(ModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonCreateSerializers

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return SeasonGetSerializers
        return super().get_serializer_class()
