from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from championship.models import Championship, Season
from championship.serializers import ChampionshipSerializers, SeasonCreateSerializers, SeasonGetSerializers
from clubs.serializers import ClubGetSerializers
from matches.models import create_matches_by_season


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

    @action(['POST'], detail=True)
    def generate_matches(self, request, pk):
        season = self.get_object()
        if season.matches_exists:
            return Response(status=400, data={'error': 'Matches already created'})
        create_matches_by_season(season)
