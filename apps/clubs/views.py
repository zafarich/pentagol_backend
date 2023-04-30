from rest_framework.viewsets import ModelViewSet

from clubs.models import Club
from clubs.serializers import ClubSerializers, ClubWithLastMatchesSerializers, ClubGetSerializers


class ClubModelViewSet(ModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializers

    def get_serializer_class(self):
        if self.request.GET.get('last_matches', 0):
            return ClubWithLastMatchesSerializers
        if self.request.method in ['GET']:
            return ClubGetSerializers

        return super().get_serializer_class()
