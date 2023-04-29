from rest_framework import serializers

from extra.models import Language


class LanguageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = [
            'id',
            'label',
            'key',
        ]

        read_only_fields = ['id']
