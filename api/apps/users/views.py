from django.conf import settings
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from djoser.views import UserViewSet
from typing import Optional


def get_cookie_settings(max_age: int, httponly: bool = True) -> dict:
    return {
        'path': settings.COOKIE_PATH,
        'secure': settings.COOKIE_SECURE,
        'samesite': settings.COOKIE_SAMESITE,
        'httponly': httponly,
        'max_age': max_age,
    }


def set_auth_cookies(response: Response, access_token: str, refresh_token: Optional[str]) -> None:
    access_token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
    response.set_cookie('access', access_token, **get_cookie_settings(access_token_lifetime, settings.COOKIE_HTTPONLY))

    if refresh_token:
        refresh_token_lifetime = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()
        response.set_cookie('refresh', refresh_token,
                            **get_cookie_settings(refresh_token_lifetime, settings.COOKIE_HTTPONLY))

    response.set_cookie('logged_in', 'true', **get_cookie_settings(access_token_lifetime, False))


def clear_auth_cookies(response: Response) -> Response:
    response.delete_cookie('access')
    response.delete_cookie('refresh')
    response.delete_cookie('logged_in')
    return response


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        token_response = super().post(request, *args, **kwargs)

        if token_response.status_code == status.HTTP_200_OK:
            access_token = token_response.data.get('access')
            refresh_token = token_response.data.get('refresh')

            if access_token and refresh_token:
                set_auth_cookies(token_response, access_token, refresh_token)
                token_response.data.pop('access', None)
                token_response.data.pop('refresh', None)
                token_response.data['message'] = 'Login Successful.'
            else:
                token_response.data['message'] = 'Login Failed.'

        return token_response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        refresh_token = request.COOKIES.get('refresh')

        if refresh_token:
            request.data['refresh'] = refresh_token

        refresh_response = super().post(request, *args, **kwargs)

        if refresh_response.status_code == status.HTTP_200_OK:
            access_token = refresh_response.data.get('access')
            refresh_token = refresh_response.data.get('refresh')

            if access_token and refresh_token:
                set_auth_cookies(refresh_response, access_token, refresh_token)
                refresh_response.data.pop('access', None)
                refresh_response.data.pop('refresh', None)
                refresh_response.data['message'] = 'Access tokens refreshed successfully.'
            else:
                refresh_response.data['message'] = 'Access or refresh tokens not found in refresh response data.'
                print('Access of refresh token not found in refresh response data.')

        return refresh_response


class LogoutAPIView(APIView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        response = Response(status=status.HTTP_204_NO_CONTENT)
        return clear_auth_cookies(response)


class CustomUserViewSet(UserViewSet):
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return clear_auth_cookies(response)
