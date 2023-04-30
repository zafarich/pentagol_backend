from django.db.models import Q
from rest_framework import serializers

from championship.serializers import ChampionshipPartialSerializers
from clubs.models import Club
from matches.models import Match


class ClubSerializers(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = [
            'id',
            'title',
            'image',
            'championship',
            'coach',
        ]

        read_only_fields = ['id']


class ClubGetSerializers(serializers.ModelSerializer):
    championship = ChampionshipPartialSerializers(read_only=True)

    class Meta:
        model = Club
        fields = [
            'id',
            'title',
            'image',
            'championship',
            'coach',
        ]

        read_only_fields = ['id']


class ClubPartialSerializers(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = [
            'id',
            'title',
            'image',
        ]


class ClubWithLastMatchesSerializers(serializers.ModelSerializer):
    last_five_matches = serializers.SerializerMethodField()

    class Meta:
        model = Club
        fields = [
            'id',
            'title',
            'image',
            'last_five_matches',
        ]

    def get_last_five_matches(self, obj):
        matches = Match.objects.filter((Q(away_club_id=obj.id) | Q(home_club_id=obj.id)
                                        & Q(is_started=True))) \
            .order_by('-tour', '-date').values('away_club_id', 'home_club_id', 'home_goals', 'away_goals')
        result = []
        for match in matches:
            if match['away_goals'] == match['home_goals']:
                result.append(0)
            if match['away_club_id'] == obj.id:
                result.append(
                    match['away_goals'] > match['home_goals']
                )
            if match['home_club_id'] == obj.id:
                result.append(
                    match['home_goals'] > match['away_goals']
                )

        return result
