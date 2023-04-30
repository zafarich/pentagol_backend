from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from matches.models import Match
from matches.serializers import MatchSerializers, MatchGETSerializers


class MatchModelViewSet(ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializers
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ['season__championship', 'tour']

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return MatchGETSerializers
        return super().get_serializer_class()
