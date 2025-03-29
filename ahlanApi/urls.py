from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from rest_framework import permissions
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from all.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="CRM API",
        default_version='v1',
        description="Mall official site description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="soyibnazarovhoji@gmail.com"),
        license=openapi.License(name="No License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = DefaultRouter()
router.register(r'objects', ObjectViewSet)
router.register(r'apartments', ApartmentViewSet)
router.register(r'users', UserViewSet)
router.register(r'expense-types', ExpenseTypeViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'expenses', ExpenseViewSet)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
app_name = 'all'
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)