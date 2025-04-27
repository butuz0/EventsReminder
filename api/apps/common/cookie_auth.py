from django.conf import settings
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication, AuthUser
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import Token


class CookieAuthentication(JWTAuthentication):
    def authenticate(self, request: Request):
        header = self.get_header(request)
        
        token = None
        if header is not None:
            token = self.get_raw_token(header)
        elif settings.COOKIE_NAME in request.COOKIES:
            token = request.COOKIES.get(settings.COOKIE_NAME)

        if token is not None:
            try:
                validated_token = self.get_validated_token(token)
                return self.get_user(validated_token), validated_token
            except TokenError as e:
                print(f'Token validation error: {str(e)}')
                
        return None
