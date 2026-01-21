from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mfc.views import (
    OfficeViewSet,
    ServiceViewSet,
    AppointmentViewSet,
    home,  
)

router = DefaultRouter()
router.register('offices', OfficeViewSet)
router.register('services', ServiceViewSet)
router.register('appointments', AppointmentViewSet)

urlpatterns = [
    path('', home, name='home'),            
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]



