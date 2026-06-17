from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mfc.views import (
    OfficeViewSet,
    ServiceViewSet,
    AppointmentViewSet,
    home,  
    login_view,
    register_view,
    logout_view,
)

router = DefaultRouter()
router.register('offices', OfficeViewSet)
router.register('services', ServiceViewSet)
router.register('appointments', AppointmentViewSet, basename='appointments')

urlpatterns = [
    path('', home, name='home'),            
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    
    # Пути для авторизации/регистрации оператора и клиентов
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
]