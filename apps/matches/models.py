from datetime import datetime, date, timedelta
import random

from django.db import models
from django.db.models import Q
from rest_framework.exceptions import ValidationError

from clubs.models import Club


class Match(models.Model):
    away_club = models.ForeignKey('clubs.Club', on_delete=models.SET_NULL, null=True, related_name='match_away')
    home_club = models.ForeignKey('clubs.Club', on_delete=models.SET_NULL, null=True, related_name='match_home')
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(default=None, null=True)
    tour = models.PositiveIntegerField()
    period = models.PositiveIntegerField()
    away_goals = models.IntegerField(default=None, null=True)
    home_goals = models.IntegerField(default=None, null=True)
    season = models.ForeignKey('championship.Season', on_delete=models.PROTECT, related_name='match', null=True)

    @property
    def match_score(self):
        if self.is_started and self.away_goals is None and self.home_goals is None:
            return '0 - 0'

        return f'{self.away_goals if self.away_goals is not None else ""} - {self.home_goals if self.home_goals is not None else ""}'

    @property
    def is_started(self):
        _date = self.date
        _time = self.time
        match_date = datetime(_date.year, _date.month, _date.day, _time.hour, _time.minute).timestamp()
        return match_date <= datetime.now().timestamp()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.home_club_id == self.away_club_id or self.home_club_id is None or self.away_club_id is None:
            raise ValidationError(detail={'Enter clubs correctly'})
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        ordering = ['tour', 'date']


def get_weeks_of_season(start_date, week_days, tours_count):
    week_days = [int(x) - 1 for x in week_days]
    weeks = []
    d = start_date
    d += timedelta(days=week_days[0] - d.weekday())  # weekday 0-index
    t_c = 1
    while t_c <= tours_count:
        weeks.append(d)
        d += timedelta(days=7)
        t_c += 1
    return weeks


def get_random_club(club, clubs):
    _clubs = [x for x in clubs if x != club]
    _club = random.choice(_clubs)
    return _club


def create_matches_by_season(season):
    tours_count = season.tours_count
    matches_count = season.matches_count
    weeks = get_weeks_of_season(
        season.start_date,
        season.match_days.split('-'),
        tours_count
    )
    weeks_1, weeks_2 = weeks[:int(len(weeks) / 2)], weeks[int(len(weeks) / 2):]

    clubs: list = list(Club.objects.filter(championship_id=season.championship_id).values_list('id', flat=True))

    period_tour = 0
    for week in weeks_1:  # 1-davra, period 1
        period_tour += 1
        _clubs1 = clubs.copy()
        while len(_clubs1) > 1:
            _club1 = random.choice(_clubs1)
            _club2 = get_random_club(_club1, _clubs1)

            if Match.objects.filter(season_id=season.id, period=1).count() == int(matches_count / 2):
                break

            if Match.objects.filter(
                    Q(season_id=season.id, period=1, home_club_id=_club1, away_club_id=_club2) |
                    Q(season_id=season.id, period=1, home_club_id=_club2, away_club_id=_club1)
            ).exists():
                if len(_clubs1) == 2 and week != weeks_1[-1]:
                    _clubs1 = clubs.copy()
                    Match.objects.filter(season_id=season.id, period=1, tour=period_tour).delete()
                continue
            else:
                _clubs1.remove(_club1)
                _clubs1.remove(_club2)
                playing_clubs = [_club1, _club2]
                random.shuffle(playing_clubs)
                Match.objects.create(
                    away_club_id=playing_clubs[0],
                    home_club_id=playing_clubs[1],
                    date=week + timedelta(days=random.choice([0, 1])),
                    period=1,
                    tour=period_tour,
                    season_id=season.id
                )
    for week in weeks_2:  # 2-davra, period 2
        period_tour += 1
        _clubs2 = clubs.copy()
        while len(_clubs2) > 1:
            _club1 = random.choice(_clubs2)
            _club2 = get_random_club(_club1, _clubs2)

            if Match.objects.filter(season_id=season.id, period=2).count() == int(matches_count / 2):
                break

            if Match.objects.filter(
                    Q(season_id=season.id, period=2, home_club_id=_club1, away_club_id=_club2) |
                    Q(season_id=season.id, period=2, home_club_id=_club2, away_club_id=_club1)
            ).exists():
                if len(_clubs2) == 2 and week != weeks_2[-1]:
                    _clubs2 = clubs.copy()
                    Match.objects.filter(season_id=season.id, period=2, tour=period_tour).delete()
                continue
            else:
                _clubs2.remove(_club1)
                _clubs2.remove(_club2)
                try:
                    match = Match.objects.get(season_id=season.id, period=1, home_club_id=_club1, away_club_id=_club2)
                except Match.DoesNotExist:
                    match = Match.objects.get(season_id=season.id, period=1, home_club_id=_club2, away_club_id=_club1)
                home_club = match.home_club_id
                away_club = match.away_club_id
                Match.objects.create(
                    away_club_id=home_club,
                    home_club_id=away_club,
                    date=week + timedelta(days=random.choice([0, 1])),
                    period=2,
                    tour=period_tour,
                    season_id=season.id
                )
