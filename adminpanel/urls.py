from django.urls import path
from . import views

urlpatterns = [

    path('users/<int:user_id>/update-role/', views.update_user_role, name='update_user_role'),

    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('students/', views.student_list, name='student_list'),
    path('students/create/', views.student_create, name='student_create'),
    path('students/<int:student_id>/', views.student_detail, name='student_detail'),  # New URL pattern
    path('students/<int:student_id>/edit/', views.student_update, name='student_update'),
    path('students/<int:student_id>/delete/', views.student_delete, name='student_delete'),

     path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/<int:teacher_id>/', views.teacher_detail, name='teacher_detail'),
    path('teachers/create/', views.teacher_create, name='teacher_create'),
    path('teachers/<int:teacher_id>/update/', views.teacher_update, name='teacher_update'),
    path('teachers/<int:teacher_id>/delete/', views.teacher_delete, name='teacher_delete'),

    # Assignment Views
    path('assignments/', views.assignment_list, name='assignment_list'),
    path('assignments/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    path('assignments/create/', views.assignment_create, name='assignment_create'),
    path('assignments/<int:assignment_id>/update/', views.assignment_update, name='assignment_update'),
    path('assignments/<int:assignment_id>/delete/', views.assignment_delete, name='assignment_delete')

]
