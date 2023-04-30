from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)

        data['access'] = str(refresh.access_token)
        data['user_data'] = {
            'username': self.user.username
        }

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user, context={'request': self.context['request']})

        return data


class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
