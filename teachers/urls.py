from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),

    path('assignments/create/', views.create_assignment, name='create_assignment'),
    path('assignments/', views.teacher_assignments, name='teacher_assignments'),
    path('assignments/<int:assignment_id>/update/', views.update_assignment, name='update_assignment'),
    path('assignments/<int:assignment_id>/delete/', views.delete_assignment, name='delete_assignment'),
    path('assignments/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),

    path('submissions/', views.teacher_submissions, name='teacher_submissions'),

    path('attendance/today/', views.view_today_attendance, name='view_today_attendance'),
    path('attendance/student/', views.view_student_attendance, name='view_student_attendance'),
   

]
