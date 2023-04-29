from datetime import datetime

from django.db import models


class Match(models.Model):
    away_club = models.ForeignKey('clubs.Club', on_delete=models.SET_NULL, null=True, related_name='match_away')
    home_club = models.ForeignKey('clubs.Club', on_delete=models.SET_NULL, null=True, related_name='match_home')
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(default=None)
    tour = models.PositiveIntegerField()
    away_gols = models.IntegerField(default=None)
    home_gols = models.IntegerField(default=None)
    season = models.ForeignKey('championship.Season', on_delete=models.PROTECT, related_name='match', null=True)

    @property
    def match_score(self):
        return f'{self.away_gols if self.away_gols is not None else ""} - {self.home_gols if self.home_gols is not None else ""}'

    @property
    def is_started(self):
        _date = self.date
        _time = self.time
        match_date = datetime(_date.year, _date.month, _date.day, _time.hour, _time.minute).timestamp()
        return match_date <= datetime.now().timestamp()
