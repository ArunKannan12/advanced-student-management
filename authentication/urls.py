from django.urls import path
from . import views
urlpatterns = [
    # Authentication URLs
    path('',views.login_view,name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    
    # Password Reset URLs
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('reset-password/<str:token>/', views.reset_password_view, name='reset_password'),
    # Email Verification URL (for when user clicks on verification link in email)
    path('email-verification/<str:uidb64>/<str:token>/', views.email_verification, name='email_verification'),
   
]