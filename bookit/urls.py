from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings

# drf_yasg imports for swagger/openapi
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Bookit API",
        default_version='v1',
        description="API documentation for Bookit",
        terms_of_service="https://example.com/terms/",
        contact=openapi.Contact(
            name="Bookit API Support",
            email="support@example.com",
            url="https://example.com",
        ),
        license=openapi.License(
            name="MIT", url="https://opensource.org/licenses/MIT"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('', include('occasions.urls')),
    path('', include('reservations.urls')),
]

# Only expose the interactive documentation when DEBUG is True
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$',
                schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('swagger/', schema_view.with_ui('swagger',
             cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc',
             cache_timeout=0), name='schema-redoc'),
    ]
