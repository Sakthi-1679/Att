from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Departments
    path('departments/', views.department_list, name='department_list'),
    path('departments/add/', views.department_create, name='department_create'),
    path('departments/<int:pk>/edit/', views.department_edit, name='department_edit'),

    # Users
    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.user_create, name='user_create'),
    path('users/<int:pk>/edit/', views.user_edit, name='user_edit'),

    # Students
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_create, name='student_create'),
    path('students/<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),

    # Attendance
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
    path('attendance/sessions/', views.sessions_list, name='sessions_list'),
    path('attendance/sessions/<int:pk>/', views.session_detail, name='session_detail'),

    # Edit Requests
    path('attendance/edit-requests/', views.edit_request_list, name='edit_request_list'),
    path('attendance/edit-requests/create/<int:record_id>/', views.create_edit_request, name='create_edit_request'),
    path('attendance/edit-requests/<int:pk>/review/', views.review_edit_request, name='review_edit_request'),

    # Reports
    path('reports/', views.attendance_report, name='attendance_report'),
    path('reports/daily/', views.daily_summary, name='daily_summary'),
    path('reports/export/excel/', views.export_excel, name='export_excel'),
    path('reports/export/pdf/', views.export_pdf, name='export_pdf'),
]
