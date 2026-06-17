from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from django.utils.timezone import now
from django.shortcuts import render
from django.db.models import Count

from .models import Office, Service, Appointment
from .serializers import (
    OfficeSerializer,
    ServiceSerializer,
    AppointmentSerializer
)
from .filters import AppointmentFilter


class StandardPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'


# 🌟 КАСТОМНЫЕ ПРАВА ДОСТУПА ДЛЯ РАЗДЕЛЕНИЯ РОЛЕЙ (Пункт 1 задания)
class IsAdminOrReadOnly(permissions.BasePermission):
    """Права для Администратора: редактирование разрешено только персоналу (admin), остальные роли могут только читать."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class AppointmentPermission(permissions.BasePermission):
    """Права для Записей (Appointment):
    - Администратор и Оператор могут видеть все записи.
    - Клиент (даже анонимный) может создавать запись (POST).
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True  # Клиент/заявитель может создать талон
        
        # Просмотр, изменение и удаление — только для сотрудников (Администратор/Оператор)
        return request.user and (request.user.is_staff or request.user.groups.filter(name='Operators').exists())


# 🏢 ВЬЮСЕТ ОФИСОВ
class OfficeViewSet(viewsets.ModelViewSet):
    # 5️⃣ Аннотация: Подсчет количества услуг в офисе
    queryset = Office.objects.annotate(total_services=Count('services')).all()
    serializer_class = OfficeSerializer
    pagination_class = StandardPagination
    # Роли: Администратор настраивает офисы, Клиенты и Операторы только смотрят
    permission_classes = [IsAdminOrReadOnly]


# 🛠️ ВЬЮСЕТ УСЛУГ
class ServiceViewSet(viewsets.ModelViewSet):
    # 3️⃣ Оптимизация select_related + 5️⃣ Аннотация: Количество записей на услугу
    queryset = Service.objects.select_related('office').annotate(
        total_appointments=Count('appointments')
    ).all()
    serializer_class = ServiceSerializer
    pagination_class = StandardPagination
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']
    # Роли: Администратор управляет списком услуг, Клиенты и Операторы ищут нужные
    permission_classes = [IsAdminOrReadOnly]


# 🎫 ВЬЮСЕТ ЗАПИСЕЙ (ТАЛОНОВ)
class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    pagination_class = StandardPagination
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter
    ]
    filterset_class = AppointmentFilter
    search_fields = ['full_name', 'email']
    # Роли: Применяем гибкое разделение прав для Клиента, Оператора и Админа
    permission_classes = [AppointmentPermission]

    # 3️⃣ Оптимизация: Подгружаем связанные данные за один SQL-запрос
    def get_queryset(self):
        return Appointment.objects.select_related('service__office').all()

    # 4.2️⃣ Контекст: Передача баннера-сообщения в сериализатор
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['banner_text'] = "Внимание: Пожалуйста, приходите за 10 минут до начала приема!"
        return context

    # 🧑‍✈️ Роль Оператора: Экшен для просмотра записей на сегодня
    @action(methods=['GET'], detail=False)
    def today(self, request):
        today = now().date()
        # Используем get_queryset() для сохранения оптимизации select_related
        qs = self.get_queryset().filter(
            appointment_date__date=today
        )
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


# 🏠 ГЛАВНАЯ СТРАНИЦА
def home(request):
    return render(request, 'mfc/home.html')


from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect

# Страница регистрации
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Автоматически логиним после регистрации
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'mfc/register.html', {'form': form})

# Страница авторизации (Вход)
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'mfc/login.html', {'form': form})

# Выход из системы
def logout_view(request):
    logout(request)
    return redirect('home')