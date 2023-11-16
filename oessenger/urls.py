from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

SchemaView = get_schema_view(
    openapi.Info(
        title="Oessenger API",
        default_version='v1',
        description="chat app",
        contact=openapi.Contact(email="omaramin622@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/swagger<format>/', SchemaView.without_ui(cache_timeout=0),
         name='schema-json'),
    path('api/swagger/', SchemaView.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('api/redoc/', SchemaView.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),

    path('api/', include('users.urls')),
]
