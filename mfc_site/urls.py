from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mfc.views import (
    OfficeViewSet,
    ServiceViewSet,
    AppointmentViewSet,
    book_appointment_view,
    home,  
    login_view,
    register_view,
    logout_view,
    services_list_view,
)

router = DefaultRouter()
router.register('offices', OfficeViewSet)
router.register('services', ServiceViewSet)
router.register('appointments', AppointmentViewSet, basename='appointments')

urlpatterns = [
    path('', home, name='home'),            
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    
    # Новые HTML-страницы для клиентов
    path('services/', services_list_view, name='services_list_html'),
    path('services/book/<int:service_id>/', book_appointment_view, name='book_appointment'),
    
    # Авторизация
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
]