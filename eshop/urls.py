from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from app_eshop.viewsets import PersonViewSet, ProductViewSet, PurchasedItemViewSet

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


router = DefaultRouter()
router.register('people', PersonViewSet, basename='people')
router.register('products', ProductViewSet, basename='products')
router.register('cart', PurchasedItemViewSet, basename='cart')

schema_view = get_schema_view(
   openapi.Info(
      title="E-Shop v1.0 - APIs Docs",
      default_version='v1',
      description="REST APIs for E-Shop platform",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('docs/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
