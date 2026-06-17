from django.contrib import admin
from import_export.admin import ExportMixin
from import_export import resources

from .models import Office, Service, Appointment


class AppointmentResource(resources.ModelResource):

    def get_export_queryset(self, request):
        # Экспортируем только записи в активные офисы
        return Appointment.objects.filter(
            service__office__is_active=True
        )

    def dehydrate_service(self, obj):
        return obj.service.title

    def dehydrate_office(self, obj):
        return obj.service.office.name

    class Meta:
        model = Appointment
        fields = (
            'id',
            'full_name',
            'email',
            'appointment_date',
            'service',
        )


# Inline отображение услуг внутри карточки Офиса МФЦ
class ServiceInline(admin.TabularInline):
    model = Service
    extra = 0


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    fields = ('name', 'address', 'is_active')
    inlines = [ServiceInline]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'office', 'duration_minutes')
    list_filter = ('office',)
    search_fields = ('title',)
    fields = ('office', 'title', 'description', 'duration_minutes')


@admin.register(Appointment)
class AppointmentAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = AppointmentResource
    list_display = ('full_name', 'service', 'appointment_date')
    list_filter = ('service__office', 'service')  # Фильтрация по офисам и услугам
    search_fields = ('full_name', 'email')