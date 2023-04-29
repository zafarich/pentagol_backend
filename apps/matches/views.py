from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from matches.models import Match
from matches.serializers import MatchSerializers


class MatchModelViewSet(ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializers
