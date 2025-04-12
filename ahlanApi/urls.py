from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from all.views import (
    ObjectViewSet, ApartmentViewSet, UserViewSet, ExpenseTypeViewSet,
    SupplierViewSet, ExpenseViewSet, PaymentViewSet, UserPaymentViewSet,
    DocumentViewSet, SupplierPaymentViewSet, CustomTokenObtainPairView
)
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'objects', ObjectViewSet)
router.register(r'apartments', ApartmentViewSet)
router.register(r'users', UserViewSet)
router.register(r'expense-types', ExpenseTypeViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'user-payments', UserPaymentViewSet)
router.register(r'supplier-payments', SupplierPaymentViewSet)
router.register(r'documents', DocumentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]