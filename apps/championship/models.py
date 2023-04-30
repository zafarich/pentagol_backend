from datetime import datetime

from django.db import models
from django.db.models.functions import Coalesce
from rest_framework.exceptions import ValidationError


def last_sort_number():
    last_number = Championship.objects.all().aggregate(sort_max=
                                                       Coalesce(models.Max('sort'), models.Value(0),
                                                                output_field=models.IntegerField()))['sort_max'] + 1
    return last_number


class Championship(models.Model):
    title = models.JSONField()
    image = models.ImageField(upload_to='championship/')
    sort = models.IntegerField(unique=True, default=last_sort_number)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)

    @property
    def championship_status(self):
        season_started = Season.objects.filter(championship_id=self.id, is_started=True).exists()
        return season_started

    @property
    def actual_season(self):
        try:
            season = Season.objects.get(championship_id=self.id, is_started=True)
            return season
        except Season.DoesNotExist:
            return None

    def all_clubs(self):
        return self.club.all()

    class Meta:
        ordering = ['sort']


class Season(models.Model):
    season_years = models.CharField(max_length=25, blank=True)
    start_date = models.DateField(blank=True)
    is_started = models.BooleanField(default=False)
    championship = models.ForeignKey('Championship', on_delete=models.PROTECT, related_name='season', blank=True)
    match_days = models.CharField(max_length=15, default='6-7')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.start_date is not None:
            if self.start_date <= datetime.today().date():
                raise ValidationError(detail={'Start date cannot be less than today'})

        if self.is_started is True:
            started_seasons_exists = Season.objects.filter(is_started=True,
                                                           championship_id=self.championship_id).exists()
            if started_seasons_exists:
                raise ValidationError(detail={'Started season already exists'})
        super().save(force_insert, force_update, using, update_fields)

    @property
    def matches_exists(self):
        return self.match.all().exists()

    @property
    def tours_count(self):
        count = self.championship.club.all().count()
        return (count - 1) * 2 if count else 0

    @property
    def matches_count(self):
        count = self.championship.club.all().count()
        return count * (count - 1) if count else 0

    class Meta:
        ordering = ['-id']
