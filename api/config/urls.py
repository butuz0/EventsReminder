from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import IsAuthenticated


schema_view = get_schema_view(
    openapi.Info(
        title='KPI Remind',
        default_version='v1',
        description='Event planner and reminder app for KPI',
        contact=openapi.Contact(email='y.o.oryshchenko@gmail.com'),
        license=openapi.License(name='MIT License'),
    ),
    public=False,
    permission_classes=[IsAuthenticated],
)


urlpatterns = [
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
    path(settings.ADMIN_URL, admin.site.urls),
    path('api/v1/units/', include('apps.units.urls')),
]
