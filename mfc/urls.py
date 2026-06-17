from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mfc.views import OfficeViewSet, ServiceViewSet, AppointmentViewSet, home

# 1. Создаём роутер и регистрируем ViewSet'ы приложения МФЦ
router = DefaultRouter()
router.register('offices', OfficeViewSet)
router.register('services', ServiceViewSet)
router.register('appointments', AppointmentViewSet)

# 2. Связываем пути: главная страница, админка и префикс api/
urlpatterns = [
    path('', home, name='home'),  # Главная HTML-страница
    path('admin/', admin.site.urls),  # Панель администратора Django
    path('api/', include(router.urls)),  # Все эндпоинты нашего REST API
]