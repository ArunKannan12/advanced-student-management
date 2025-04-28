from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from .models import Attendance
from student.models import Student

@receiver(user_logged_in)
def mark_attendance_on_login(sender, request, user, **kwargs):
    # Check if the user is a student
    if hasattr(user, 'student'):  # Assuming the user has a related Student model
        student = user.student
        today = timezone.now().date()
        
        # Check if attendance for today is already marked
        if not Attendance.objects.filter(student=student, date=today).exists():
            # Mark attendance as 'Present' or any other status (e.g., 'Late')
            Attendance.objects.create(student=student, date=today, status='P')  # You can use 'L' for Late
