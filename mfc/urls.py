from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mfc.views import (
    OfficeViewSet, 
    ServiceViewSet, 
    AppointmentViewSet, 
    home,
    register_view,
    login_view,
    logout_view,
    services_list_view,
    book_appointment_view
)

# 1. Создаём роутер и регистрируем ViewSet'ы приложения МФЦ
router = DefaultRouter()
router.register('offices', OfficeViewSet)
router.register('services', ServiceViewSet)
router.register('appointments', AppointmentViewSet)

# 2. Связываем пути: главная страница, админка и префикс api/
urlpatterns = [
    path('', home, name='home'),  # Главная HTML-страница
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('services/', services_list_view, name='services_list_html'),
    path('book/<int:service_id>/', book_appointment_view, name='book_appointment'),
    path('admin/', admin.site.urls),  # Панель администратора Django
    path('api/', include(router.urls)),  # Все эндпоинты нашего REST API
]