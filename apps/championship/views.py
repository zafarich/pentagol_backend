import datetime

from django.db.models import Q, Sum, Value, IntegerField
from django.db.models.functions import Coalesce
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from championship.models import Championship, Season
from championship.serializers import ChampionshipSerializers, SeasonCreateSerializers, SeasonGetSerializers
from clubs.models import Club
from matches.models import create_matches_by_season, Match
from matches.serializers import MatchGETSerializers
from pentagol.settings import CURRENT_HOST


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

    @action(['GET'], detail=True)
    def table(self, request, pk):  # ORM code yozishga vaqt yetmadi
        championship = self.get_object()
        actual_season = championship.actual_season
        result = []
        if actual_season is not None:
            clubs = Club.objects.filter(championship_id=pk)
            for club in clubs:
                games = Match.objects.filter(
                    Q(season_id=actual_season.id, home_club_id=club.id, home_goals__isnull=False) |
                    Q(season_id=actual_season.id, away_club_id=club.id, home_goals__isnull=False))
                game_score = 0
                t_n = 0

                for g in games:
                    if g.home_club_id == club.id:
                        if g.home_goals > g.away_goals:
                            game_score += 3
                        t_n += g.home_goals - g.away_goals
                    if g.away_club_id == club.id:
                        if g.home_goals < g.away_goals:
                            game_score += 3
                        t_n += g.away_goals - g.home_goals
                    if g.home_goals == g.away_goals:
                        game_score += 1

                game_count = games.count()

                result.append({
                    'id': club.id,
                    'title': club.title,
                    'game_count': game_count,
                    'score': game_score,
                    't_n': t_n,
                    'image': CURRENT_HOST + club.image.url
                })

                result = sorted(result, key=lambda x: (x['score'], x['t_n']), reverse=True)

                for ind, res in enumerate(result):
                    if ind == 0:
                        continue
                    if result[ind - 1]['score'] == result[ind]['score'] and result[ind - 1]['t_n'] == result[ind][
                        't_n']:
                        cl_1_home_goals = \
                            Match.objects.filter(season_id=actual_season.id,
                                                 home_club_id=result[ind - 1]['id']).aggregate(
                                summ=Coalesce(Sum('home_goals'), Value(0), output_field=IntegerField()))['summ']
                        cl_1_away_goals = \
                            Match.objects.filter(season_id=actual_season.id,
                                                 away_club_id=result[ind - 1]['id']).aggregate(
                                summ=Coalesce(Sum('away_goals'), Value(0), output_field=IntegerField()))['summ']
                        cl_2_home_goals = \
                            Match.objects.filter(season_id=actual_season.id, home_club_id=result[ind]['id']).aggregate(
                                summ=Coalesce(Sum('home_goals'), Value(0), output_field=IntegerField()))['summ']
                        cl_2_away_goals = \
                            Match.objects.filter(season_id=actual_season.id, away_club_id=result[ind]['id']).aggregate(
                                summ=Coalesce(Sum('away_goals'), Value(0), output_field=IntegerField()))['summ']

                        if cl_1_home_goals + cl_1_away_goals < cl_2_home_goals + cl_2_away_goals:
                            result[ind - 1], result[ind] = result[ind], result[ind - 1]

            return Response(status=200, data=result)
        else:
            return Response(status=200, data={'Season has not started'})


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
