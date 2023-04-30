from django.db.models import Q
from rest_framework import serializers

from championship.serializers import ChampionshipPartialSerializers
from clubs.models import Club
from matches.models import Match
from pentagol.settings import CURRENT_HOST


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
    image = serializers.SerializerMethodField()

    class Meta:
        model = Club
        fields = [
            'id',
            'title',
            'image',
        ]

    def get_image(self, obj):
        return CURRENT_HOST + obj.image.url
