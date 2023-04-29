from django.urls import include, path
from rest_framework.routers import SimpleRouter

from clubs.views import ClubModelViewSet

router = SimpleRouter()
router.register('', ClubModelViewSet, 'clubs')

urlpatterns = [
    path('', include(router.urls)),
]
