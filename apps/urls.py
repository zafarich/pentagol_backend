from django.urls import include, path

from pentagol.settings import LOCAL_APPS

# Apps urls

urlpatterns = [path(f'{x}/', include((f'{x}.urls', f'{x}'), f'{x}'))
               for x in LOCAL_APPS]
