from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import IsAuthenticated


schema_view = get_schema_view(
    openapi.Info(
        title='KPI Notify',
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
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('apps.users.urls')),
    path('api/v1/units/', include('apps.units.urls')),
    path('api/v1/events/', include('apps.events.urls')),
    path('api/v1/notifications/', include('apps.notifications.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
