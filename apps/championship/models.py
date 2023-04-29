from datetime import datetime

from django.db import models
from rest_framework.exceptions import ValidationError


def last_sort_number():
    last_number = Championship.objects.all().aggregate(models.Max('rating'))['sort__max'] + 1
    return last_number


class Championship(models.Model):
    title = models.JSONField()
    image = models.ImageField(upload_to='championship')
    sort = models.IntegerField(unique=True, default=last_sort_number)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)


class Season(models.Model):
    season_years = models.CharField(max_length=25)
    start_date = models.DateField()
    is_started = models.BooleanField(default=False)
    championship = models.ForeignKey('Championship', on_delete=models.PROTECT, related_name='season')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.start_date is not None:
            if self.start_date <= datetime.today().date():
                raise ValidationError(detail={'Start date cannot be less than today'})

        if self.is_started is True:
            started_seasons_exists = Season.objects.filter(is_started=True, championship_id=self.championship_id).exists()
            if started_seasons_exists:
                raise ValidationError(detail={'Started season already exists'})
        super().save(force_insert, force_update, using, update_fields)
