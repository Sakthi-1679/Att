from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Department, Student, Period, AttendanceSession, AttendanceRecord, EditRequest


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'department', 'is_active')
    list_filter = ('role', 'department')
    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role', 'department')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Info', {'fields': ('role', 'department')}),
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('register_number', 'name', 'department', 'parent_phone', 'is_active')
    list_filter = ('department', 'is_active')
    search_fields = ('register_number', 'name', 'email')


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ('period_number', 'start_time', 'end_time')


@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = ('date', 'period', 'department', 'marked_by', 'is_submitted')
    list_filter = ('date', 'department', 'is_submitted')


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'session', 'status', 'sms_sent')
    list_filter = ('status', 'sms_sent')


@admin.register(EditRequest)
class EditRequestAdmin(admin.ModelAdmin):
    list_display = ('requested_by', 'record', 'old_status', 'new_status', 'status', 'created_at')
    list_filter = ('status',)
