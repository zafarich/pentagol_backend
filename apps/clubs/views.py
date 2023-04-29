from rest_framework.viewsets import ModelViewSet

from clubs.models import Club
from clubs.serializers import ClubSerializers


class ClubModelViewSet(ModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializers
