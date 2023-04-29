from django.db import models


class Match(models.Model):
    away_club = models.ForeignKey('clubs.Club', on_delete=models.SET_NULL, null=True, related_name='match_away')
    home_club = models.ForeignKey('clubs.Club', on_delete=models.SET_NULL, null=True, related_name='match_home')
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(default=None)
    tur = models.PositiveIntegerField()
