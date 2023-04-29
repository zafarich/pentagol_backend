from rest_framework.viewsets import ModelViewSet

from extra.models import Language
from extra.serializers import LanguageSerializers


class LanguageModelViewSet(ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializers
