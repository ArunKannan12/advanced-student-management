from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.timezone import now
from django.core.mail import send_mail
from datetime import timedelta
from django.urls import reverse




# Manager for CustomUser
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required.")
        
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# Custom User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_joined = models.DateTimeField(auto_now_add=True)

    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'first_name', 'last_name']  # Ensure 'username' is a required field for superuser creation

    def __str__(self):
        return f"{self.email}"
    
    def delete(self, *args, **kwargs):
        self.groups.clear()
        self.user_permissions.clear()
        super().delete(*args, **kwargs)
def generate_reset_token():
    return get_random_string(32)  
    


class PasswordResetRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)
    token = models.CharField(max_length=50,default=generate_reset_token,editable=False,unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    TOKEN_VALIDITY_PERIOD = timedelta(hours=1)

    def is_valid(self):
        return now() <= self.created_at + self.TOKEN_VALIDITY_PERIOD

    def send_reset_email(self):
        reset_link = f"http://localhost:8000/reset-password/{self.token}"
        subject = "Password Reset Request"
        message = f"Hi,\n\nClick the link below to reset your password:\n{reset_link}\n\nIf you did not request this, please ignore this email."

        send_mail(
            subject,
            message,
            'arunachu962@gmail.com',
            [self.email],
            fail_silently=False,
        )
        return self.token