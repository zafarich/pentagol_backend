import datetime

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from championship.models import Championship, Season
from championship.serializers import ChampionshipSerializers, SeasonCreateSerializers, SeasonGetSerializers
from clubs.models import Club
from clubs.serializers import ClubGetSerializers
from matches.models import create_matches_by_season, Match
from matches.serializers import MatchGETSerializers


class ChampionshipModelViewSet(ModelViewSet):
    queryset = Championship.objects.all()
    serializer_class = ChampionshipSerializers

    @action(['GET'], detail=True)
    def last_matches(self, request, pk):
        championship = self.get_object()
        actual_season = championship.actual_season
        if actual_season is not None:
            this_week = datetime.datetime.today().weekday()

            today = datetime.date.today()
            start_week = datetime.date.today() - datetime.timedelta(today.weekday())
            pre_start_week = start_week - datetime.timedelta(weeks=1)
            pre_end_week = pre_start_week + datetime.timedelta(days=6)
            # entries = Entry.objects.filter(created_at__range=[start_week, end_week])

            matches = Match.objects.filter(season__championship_id=actual_season.championship_id,
                                           date__range=[pre_start_week, pre_end_week])
            matches_serializer = MatchGETSerializers(matches, many=True)
            return Response(status=200, data=matches_serializer.data)
        else:
            return Response(status=222, data={'season_has_not_started'})

    @action(['GET'], detail=True)
    def today_matches(self, request, pk):
        championship = self.get_object()
        actual_season = championship.actual_season
        if actual_season is not None:
            today = datetime.datetime.today().date()
            matches = Match.objects.filter(season__championship_id=actual_season.championship_id, date=today)
            matches_serializer = MatchGETSerializers(matches, many=True)
            return Response(status=200, data=matches_serializer.data)
        else:
            return Response(status=200, data={'Season has not started'})

    # @action(['GET'], detail=True)
    # def table(self, request, pk):
    #     championship = self.get_object()
    #     actual_season = championship.actual_season
    #     # if actual_season is not None:
    #         # clubs = Club.objects.filter(championship_id=pk)
    #         # return Response(status=200, data=matches_serializer.data)
    #     else:
    #         return Response(status=200, data={'Season has not started'})


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
        return Response(status=201, data={'success': True})
