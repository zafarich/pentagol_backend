from django.db import models
from rest_framework.exceptions import ValidationError

from championship.models import Championship


class Club(models.Model):
    title = models.CharField(max_length=127)
    image = models.ImageField(upload_to='clubs/')
    championship = models.ForeignKey('championship.Championship', on_delete=models.PROTECT, related_name='club')
    coach = models.CharField(max_length=127)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        actual_season = self.championship.actual_season
        if actual_season is not None and actual_season.is_started:
            raise ValidationError(detail={"Championship has already started. Can't create a club"})

        super().save(force_insert, force_update, using, update_fields)
