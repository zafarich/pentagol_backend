from rest_framework.viewsets import ModelViewSet

from matches.models import Match
from matches.serializers import MatchSerializers, MatchGETSerializers


class MatchModelViewSet(ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializers

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return MatchGETSerializers
        return super().get_serializer_class()
