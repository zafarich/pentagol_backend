from django.db import models


class Language(models.Model):
    label = models.CharField(max_length=25)
    key = models.CharField(max_length=10)

    class Meta:
        ordering = ['-id']
