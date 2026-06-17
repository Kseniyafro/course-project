from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from mfc.models import Office, Service, Appointment


class Command(BaseCommand):
    help = 'Автоматически заполняет базу данных тестовыми данными для МФЦ и создает учетные записи'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Очистка старых данных и пользователей...'))
        Appointment.objects.all().delete()
        Service.objects.all().delete()
        Office.objects.all().delete()
        User.objects.filter(username__in=['admin', 'operator1']).delete()

        self.stdout.write(self.style.SUCCESS('1. Создание учетных записей для демонстрации ролей...'))
        
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@mfc.ru',
            password='adminpassword'
        )
        self.stdout.write(self.style.SUCCESS('   -> Создан Администратор: admin (пароль: adminpassword)'))

        operator_user = User.objects.create_user(
            username='operator1',
            email='operator1@mfc.ru',
            password='operatorpassword',
            is_staff=True
        )
        self.stdout.write(self.style.SUCCESS('   -> Создан Оператор: operator1 (пароль: operatorpassword)'))

        self.stdout.write(self.style.SUCCESS('2. Наполнение структуры МФЦ...'))

        offices_data = [
            {"name": "МФЦ Мои Документы — Центральный", "address": "ул. Большая Семеновская, д. 38", "is_active": True},
            {"name": "МФЦ Мои Документы — Тверской", "address": "ул. Тверская, д. 12, стр. 1", "is_active": True},
            {"name": "МФЦ Мои Документы — Первомайский", "address": "ул. Первомайская, д. 52", "is_active": False},
        ]

        created_offices = []
        for office_info in offices_data:
            office = Office.objects.create(**office_info)
            created_offices.append(office)
            self.stdout.write(f'Создан офис: {office.name}')

        services_templates = [
            {"title": "Выдача и замена паспорта РФ", "description": "Оформление внутреннего паспорта гражданина РФ по достижении возраста, смене данных или утере.", "duration_minutes": 20},
            {"title": "Регистрация права собственности", "description": "Государственная регистрация прав на недвижимое имущество и сделок с ним.", "duration_minutes": 30},
            {"title": "Оформление загранпаспорта", "description": "Прием заявлений на биометрический загранпаспорт нового образца на 10 лет.", "duration_minutes": 15},
            {"title": "Подача заявления на СНИЛС", "description": "Первичное получение или замена страхового номера индивидуального лицевого счета.", "duration_minutes": 10},
        ]

        created_services = []
        for office in created_offices:
            if office.is_active:
                for src in services_templates:
                    service = Service.objects.create(
                        office=office,
                        title=src["title"],
                        description=src["description"],
                        duration_minutes=src["duration_minutes"]
                    )
                    created_services.append(service)
                self.stdout.write(f'  Добавлены базовые услуги для: {office.name}')

        self.stdout.write(self.style.SUCCESS('3. Генерация талонов (записей)...'))
        
        names = ["Иванов Иван", "Петров Петр", "Сергеев Сергей", "Аннова Анна"]
        emails = ["ivanov@example.com", "petrov@example.com", "sergeev@example.com", "anna@example.com"]

        current_date = (timezone.now() + timezone.timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)
        
        for i, service in enumerate(created_services[:4]):
            appointment_time = current_date + timezone.timedelta(hours=i)
            
            Appointment.objects.create(
                service=service,
                full_name=names[i % len(names)],
                email=emails[i % len(emails)],
                appointment_date=appointment_time
            )
            self.stdout.write(f'   Талон: {names[i]} записан на {service.title} в {appointment_time.strftime("%H:%M")}')

        self.stdout.write(self.style.SUCCESS('База данных МФЦ полностью готова к демонстрации!'))