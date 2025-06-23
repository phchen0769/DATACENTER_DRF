from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from apps.api.models import PermanentToken


class DynamicAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Api"):
            token_key = auth_header.split()[1]
            token = PermanentToken.objects.filter(key=token_key).first()
            if not token:
                raise exceptions.AuthenticationFailed("无效的长期Token")
            return (token.user, token)
        elif auth_header.startswith("Bearer"):
            # 调用 simplejwt 的认证
            return JWTAuthentication().authenticate(request)
        return None
