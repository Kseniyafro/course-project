# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import (
#     OfficeViewSet,
#     ServiceViewSet,
#     AppointmentViewSet
# )

# router = DefaultRouter()
# router.register('offices', OfficeViewSet)
# router.register('services', ServiceViewSet)
# router.register('appointments', AppointmentViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mfc.views import OfficeViewSet, ServiceViewSet, AppointmentViewSet
from mfc.views import home

# 1. Сначала создаём роутер и регистрируем ViewSet'ы
router = DefaultRouter()
router.register('offices', OfficeViewSet)
router.register('services', ServiceViewSet)
router.register('appointments', AppointmentViewSet)

# 2. Потом подключаем роутер к URL
urlpatterns = [
    path('', home),  # главная страница
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
