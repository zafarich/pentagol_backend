from rest_framework import serializers

from championship.serializers import SeasonGetSerializers
from clubs.serializers import ClubWithLastMatchesSerializers
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
            'away_goals',
            'home_goals',
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


class MatchGETSerializers(serializers.ModelSerializer):
    away_club = ClubWithLastMatchesSerializers()
    home_club = ClubWithLastMatchesSerializers()
    season = SeasonGetSerializers()

    class Meta:
        model = Match
        fields = [
            'id',
            'away_club',
            'home_club',
            'date',
            'time',
            'tour',
            'match_score',
            'season',
            'is_started',
        ]
