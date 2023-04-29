from rest_framework import serializers

from championship.models import Championship, Season


class ChampionshipSerializers(serializers.ModelSerializer):

    class Meta:
        model = Championship
        fields = [
            'id',
            'title',
            'image',
            'sort',
        ]

        read_only_fields = ['id']


class SeasonSerializers(serializers.ModelSerializer):

    class Meta:
        model = Season
        fields = [
            'id',
            'season_years',
            'start_date',
            'is_started',
        ]

        read_only_fields = ['id']
