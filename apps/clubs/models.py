from django.db import models


class Club(models.Model):
    title = models.CharField(max_length=127)
    image = models.ImageField(upload_to='clubs')
    championship = models.ForeignKey('championship.Championship', on_delete=models.PROTECT, related_name='club')
    coach = models.CharField(max_length=127)
