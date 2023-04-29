import json

from rest_framework import serializers

from championship.models import Championship, Season


class ChampionshipSerializers(serializers.ModelSerializer):
    title = serializers.JSONField(required=False)

    class Meta:
        model = Championship
        fields = [
            'id',
            'title',
            'image',
            'sort',
            'championship_status',
            'actual_season',
        ]

        read_only_fields = ['id', 'championship_status']


class ChampionshipPartialSerializers(serializers.ModelSerializer):
    title = serializers.JSONField(required=False)

    class Meta:
        model = Championship
        fields = [
            'id',
            'title',
        ]


class SeasonCreateSerializers(serializers.ModelSerializer):

    class Meta:
        model = Season
        fields = [
            'id',
            'season_years',
            'start_date',
            'championship',
            'is_started',
            'match_days',
        ]

        read_only_fields = ['id']


class SeasonGetSerializers(serializers.ModelSerializer):
    championship = ChampionshipPartialSerializers()

    class Meta:
        model = Season
        fields = [
            'id',
            'season_years',
            'start_date',
            'championship',
            'is_started',
            'match_days',
        ]
