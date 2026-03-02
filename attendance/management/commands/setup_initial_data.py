from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import time


class Command(BaseCommand):
    help = 'Set up initial data: admin user, periods, departments, and sample students'

    def handle(self, *args, **options):
        from attendance.models import CustomUser, Department, Student, Period

        self.stdout.write("Setting up initial data...")

        # Create Periods P1-P7
        period_data = [
            (1, time(9, 0),  time(9, 50)),
            (2, time(9, 50), time(10, 40)),
            (3, time(10, 40), time(11, 30)),
            (4, time(11, 30), time(12, 20)),
            (5, time(13, 10), time(14, 0)),
            (6, time(14, 0), time(14, 50)),
            (7, time(14, 50), time(15, 40)),
        ]
        for num, start, end in period_data:
            Period.objects.get_or_create(
                period_number=num,
                defaults={'start_time': start, 'end_time': end}
            )
        self.stdout.write(self.style.SUCCESS("  ✓ Periods P1-P7 created"))

        # Create Departments
        departments_data = [
            ('Computer Science Engineering', 'CSE'),
            ('Electronics and Communication Engineering', 'ECE'),
            ('Mechanical Engineering', 'MECH'),
            ('Civil Engineering', 'CIVIL'),
            ('Information Technology', 'IT'),
        ]
        depts = {}
        for name, code in departments_data:
            dept, _ = Department.objects.get_or_create(code=code, defaults={'name': name})
            depts[code] = dept
        self.stdout.write(self.style.SUCCESS("  ✓ Departments created"))

        # Create Admin user
        if not CustomUser.objects.filter(username='admin').exists():
            admin = CustomUser.objects.create_superuser(
                username='admin',
                password='admin123',
                email='admin@college.edu',
                first_name='Principal',
                last_name='Admin',
                role='admin'
            )
            self.stdout.write(self.style.SUCCESS("  ✓ Admin user created (admin / admin123)"))
        else:
            self.stdout.write("  - Admin user already exists")

        # Create Staff users
        staff_data = [
            ('staff_cse', 'staff123', 'John', 'Smith', 'CSE'),
            ('staff_ece', 'staff123', 'Jane', 'Doe', 'ECE'),
            ('staff_mech', 'staff123', 'Robert', 'Brown', 'MECH'),
        ]
        for username, password, first, last, dept_code in staff_data:
            if not CustomUser.objects.filter(username=username).exists():
                CustomUser.objects.create_user(
                    username=username, password=password,
                    first_name=first, last_name=last,
                    email=f'{username}@college.edu',
                    role='staff', department=depts.get(dept_code)
                )
        self.stdout.write(self.style.SUCCESS("  ✓ Staff users created (password: staff123)"))

        # Create Coordinator
        if not CustomUser.objects.filter(username='coordinator').exists():
            CustomUser.objects.create_user(
                username='coordinator', password='coord123',
                first_name='Coordinator', last_name='One',
                email='coordinator@college.edu',
                role='coordinator', department=depts.get('CSE')
            )
        self.stdout.write(self.style.SUCCESS("  ✓ Coordinator created (coordinator / coord123)"))

        # Create Sample Students
        students_data = [
            ('CSE001', 'Alice Johnson', 'alice@example.com', '+91-9876543210', 'CSE'),
            ('CSE002', 'Bob Williams', 'bob@example.com', '+91-9876543211', 'CSE'),
            ('CSE003', 'Carol Davis', 'carol@example.com', '+91-9876543212', 'CSE'),
            ('CSE004', 'David Wilson', 'david@example.com', '+91-9876543213', 'CSE'),
            ('CSE005', 'Eva Martinez', 'eva@example.com', '+91-9876543214', 'CSE'),
            ('ECE001', 'Frank Anderson', 'frank@example.com', '+91-9876543220', 'ECE'),
            ('ECE002', 'Grace Thomas', 'grace@example.com', '+91-9876543221', 'ECE'),
            ('ECE003', 'Henry Jackson', 'henry@example.com', '+91-9876543222', 'ECE'),
            ('MECH001', 'Iris White', 'iris@example.com', '+91-9876543230', 'MECH'),
            ('MECH002', 'Jack Harris', 'jack@example.com', '+91-9876543231', 'MECH'),
            ('IT001', 'Karen Martin', 'karen@example.com', '+91-9876543240', 'IT'),
            ('IT002', 'Leo Garcia', 'leo@example.com', '+91-9876543241', 'IT'),
        ]
        count = 0
        for reg, name, email, phone, dept_code in students_data:
            _, created = Student.objects.get_or_create(
                register_number=reg,
                defaults={
                    'name': name, 'email': email,
                    'parent_phone': phone,
                    'department': depts.get(dept_code)
                }
            )
            if created:
                count += 1
        self.stdout.write(self.style.SUCCESS(f"  ✓ {count} sample students created"))

        self.stdout.write(self.style.SUCCESS("\n✅ Initial data setup complete!"))
        self.stdout.write(self.style.WARNING("\nLogin credentials:"))
        self.stdout.write("  Admin:       admin / admin123")
        self.stdout.write("  Staff (CSE): staff_cse / staff123")
        self.stdout.write("  Coordinator: coordinator / coord123")
