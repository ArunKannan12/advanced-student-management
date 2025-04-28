from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('assignments/', views.student_assignments, name='student_assignments'),
    path('assignment/<int:assignment_id>/', views.student_assignment_detail, name='student_assignment_detail'),
    path('assignment/delete/<int:submission_id>/', views.delete_submission, name='delete_submission'),
]
