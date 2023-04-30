from datetime import datetime, date, timedelta
import random

from django.db import models
from rest_framework.exceptions import ValidationError

from clubs.models import Club


class Match(models.Model):
    away_club = models.ForeignKey('clubs.Club', on_delete=models.SET_NULL, null=True, related_name='match_away')
    home_club = models.ForeignKey('clubs.Club', on_delete=models.SET_NULL, null=True, related_name='match_home')
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(default=None)
    tour = models.PositiveIntegerField()
    away_goals = models.IntegerField(default=None)
    home_goals = models.IntegerField(default=None)
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
    d += timedelta(days=random.choice(week_days) - d.weekday())  # weekday
    t_c = 1
    while t_c <= tours_count:
        weeks.append(d)
        d += timedelta(days=7)
        t_c += 1
    return weeks


def create_matches_by_season(season):
    tours_count = season.tours_count
    weeks = get_weeks_of_season(
        season.start_date,
        season.match_days.split('-'),
        tours_count
    )
    weeks_1, weeks_2 = weeks

    clubs: list = Club.objects.filter(championship_id=season.championship_id).values_list('id', flat=True)
    for club in clubs:
        _clubs = clubs.copy()
        _clubs.remove(club)
        for tour in range(tours_count):
            day1 = weeks_1[tour]
            day2 = weeks_1
            _club2 = random.choice(_clubs)

            Match.objects.get_or_create(
                away_club_id=club,
                home_club_id=_club2,
                defaults={
                    'date': day1,
                    'time': None,
                    'tour': tour + 1,
                    'season_id': season.id
                }
            )

            Match.objects.create(
                away_club_id=_club2,
                home_club_id=club,
                defaults={
                    'date': day2,
                    'time': None,
                    'tour': tour + 1,
                    'season_id': season.id
                }
            )
            _clubs.remove(_club2)
