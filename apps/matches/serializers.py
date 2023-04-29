from rest_framework import serializers

from matches.models import Match


class MatchSerializers(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = [
            'id',
            'away_club',
            'home_club',
            'date',
            'time',
            'tur',
        ]

        read_only_fields = ['id', 'tur', 'away_club', 'home_club']
