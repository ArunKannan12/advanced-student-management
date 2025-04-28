from django.db import models
from authentication.models import CustomUser  # adjust based on your project
from django.db import models
from student.models import Student
from django.utils import timezone


class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} ({self.employee_id})"


class Assignment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    students = models.ManyToManyField(Student)  # Multiple students

    def __str__(self):
        return f"{self.title} (Due: {self.due_date})"
    
class StudentAssignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    submitted_file = models.FileField(upload_to='submissions/', blank=True, null=True)
    submitted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('student', 'assignment')  # ensures 1 student - 1 assignment entry

    def __str__(self):
        return f"{self.student.user.first_name} - {self.assignment.title}"
    

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Late'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    
    class Meta:
        unique_together = ('student', 'date')  # Ensures a student can't have multiple entries for the same day
    
    def __str__(self):
        return f"{self.student.user.username} - {self.date} - {self.get_status_display()}"