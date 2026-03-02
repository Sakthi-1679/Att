from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin (Principal)'),
        ('staff', 'Staff (Faculty)'),
        ('coordinator', 'Coordinator'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='users'
    )

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_staff_role(self):
        return self.role == 'staff'

    @property
    def is_coordinator(self):
        return self.role == 'coordinator'


class Student(models.Model):
    register_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    parent_phone = models.CharField(max_length=15)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='students')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['register_number']

    def __str__(self):
        return f"{self.register_number} - {self.name}"

    def attendance_percentage(self, start_date=None, end_date=None):
        records = AttendanceRecord.objects.filter(session__department=self.department, student=self)
        if start_date:
            records = records.filter(session__date__gte=start_date)
        if end_date:
            records = records.filter(session__date__lte=end_date)
        total = records.count()
        if total == 0:
            return 0
        present = records.filter(status='present').count()
        return round((present / total) * 100, 2)


class Period(models.Model):
    period_number = models.IntegerField(unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ['period_number']

    def __str__(self):
        return f"Period {self.period_number} ({self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')})"


class AttendanceSession(models.Model):
    date = models.DateField()
    period = models.ForeignKey(Period, on_delete=models.CASCADE, related_name='sessions')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='sessions')
    marked_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='marked_sessions')
    is_submitted = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('date', 'period', 'department')
        ordering = ['-date', 'period']

    def __str__(self):
        return f"{self.department.code} | {self.date} | Period {self.period.period_number}"


class AttendanceRecord(models.Model):
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('informed_leave', 'Informed Leave'),
    )
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, related_name='records')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present')
    sms_sent = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('session', 'student')

    def __str__(self):
        return f"{self.student.register_number} | {self.session} | {self.status}"


class EditRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, related_name='edit_requests')
    record = models.ForeignKey(AttendanceRecord, on_delete=models.CASCADE, related_name='edit_requests')
    requested_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='edit_requests_made'
    )
    approved_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='edit_requests_reviewed'
    )
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"EditRequest by {self.requested_by.username} | {self.status}"
