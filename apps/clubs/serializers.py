from rest_framework import serializers

from clubs.models import Club


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
