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
            'tour',
            'away_gols',
            'home_gols',
            'match_score',
            'is_started',
        ]

        read_only_fields = [
            'id',
            'tour',
            'away_club',
            'home_club',
            'match_score',
            'is_started'
        ]
