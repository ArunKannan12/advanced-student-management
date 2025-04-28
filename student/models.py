from django.db import models
from authentication.models import CustomUser  # adjust if your user model is elsewhere

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=20, unique=True)
    class_name = models.CharField(max_length=50)
    date_of_admission = models.DateField(auto_now_add=True)
    parent_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.first_name} - {self.roll_no} "

    