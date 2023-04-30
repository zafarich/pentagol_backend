from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from extra.models import Language
from extra.serializers import LanguageSerializers


class LanguageModelViewSet(ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializers


class ModelViewSetWithNumberPaginationViewSet(ModelViewSet):

    def get_paginated_response(self, data):
        _pagination = self.request.query_params.get('pagination', None)
        if _pagination and _pagination == 'number':
            return Response({
                'links': {
                    'next': self.paginator.get_next_link(),
                    'previous': self.paginator.get_previous_link()
                },
                'next': self.paginator.page.next_page_number() if self.paginator.page.paginator.num_pages > self.paginator.page.number else None,
                'previous': self.paginator.page.previous_page_number() if self.paginator.page.number > 1 else None,
                'count': self.paginator.page.paginator.count,
                'results': data
            })
        return super().get_paginated_response(data)

