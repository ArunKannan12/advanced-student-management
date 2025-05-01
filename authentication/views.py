from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.utils.timezone import now

from django.contrib.auth.forms import PasswordChangeForm,SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from .forms import SignupForm
from .models import CustomUser, PasswordResetRequest
from .utils import send_verification_email

import logging

logger = logging.getLogger('verification')
logger = logging.getLogger(__name__)

signer = TimestampSigner()


# Email Verification View
def send_verification_email(user, request):
    token = signer.sign(user.email)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    domain = get_current_site(request).domain
    verify_link = f"http://{domain}{reverse('email_verification', kwargs={'uidb64': uid, 'token': token})}"
    
    logger.info(f"Verification email sent to {user.email} at {now()}")

    subject = "Verify Your Email Address"
    message = render_to_string('authentication/verify_email.html', {
        'user': user,
        'verify_link': verify_link
    })

    try:
        send_mail(
        subject,
        message,
        'arunachu962@gmail.com.com',
        [user.email],
        fail_silently=False,
    )
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        messages.error(request, 'Failed to send the email.')


def email_verification(request, uidb64, token):
    try:
        # Decode the user ID from the URL
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
        
        # Unsigned token check for validity
        email_token = signer.unsign(token, max_age=60*60*24)

        # If token matches the user's email, activate the user
        if email_token == user.email:
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, "Email verified and you are now logged in!")
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'teacher':
                return redirect('teacher_dashboard')
            elif user.role == 'student':
                return redirect('student_dashboard')
            else:
                messages.error(request, 'Invalid user role.')
                return redirect('index')
        else:
            # Token mismatch, logging and informing the user
            
            messages.error(request, "The verification token is invalid or expired.")
            return redirect('login')

    except (BadSignature, SignatureExpired, get_user_model().DoesNotExist):
        # Handle invalid signatures, expired tokens, or non-existing users
        messages.error(request, "The verification link is invalid or expired.")
        return redirect('home')


def resend_verification_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = get_user_model().objects.get(email=email)
            if not user.is_active:
                send_verification_email(user,request)
                messages.success(request, 'Verification link resent. Please check your email.')
            else:
                messages.info(request, 'This account is already verified.')
        except get_user_model().DoesNotExist:
            messages.error(request, 'No account found with that email.')

    return redirect('login') 



# Signup View
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_verification_email(user, request)
            messages.info(request, 'Please check your email to verify your account.')
            
    else:
        form = SignupForm()

    return render(request, 'authentication/register.html', {'form': form})


# Login View
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            if not user.is_active:
                messages.error(request, 'Your account is not activated. Please verify your email.')
                return redirect('login')

            login(request, user)
            messages.success(request, 'Login successful!')

            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'teacher':
                return redirect('teacher_dashboard')
            elif user.role == 'student':
                return redirect('student_dashboard')
            else:
                messages.error(request, 'Invalid user role.')
                return redirect('index')
        else:
            messages.error(request, 'Invalid credentials.')

    return render(request, 'authentication/login.html')


# Forgot Password View

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = CustomUser.objects.filter(email=email).first()

        if user:
            # Clear any existing reset tokens for the user
            PasswordResetRequest.objects.filter(user=user).delete()

            reset_request = PasswordResetRequest.objects.create(user=user, email=email)
            reset_request.send_reset_email()
            logger.info(f"Password reset requested for {email}")
            messages.success(request, 'A reset link has been sent to your email.')
        else:
            logger.warning(f"Password reset attempted for non-existent email: {email}")
            messages.error(request, 'No account found with that email address.')

    return render(request, 'authentication/forgot_password.html')



# Reset Password View
@login_required
def change_password_view(request):
    if not request.user.is_authenticated:
        messages.error(request,'You must be logged in to change your password')
        return redirect('login')
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()  # Save the new password
            update_session_auth_hash(request, form.user)  # Keeps the user logged in after password change
            messages.success(request, 'Your password has been updated successfully.')
            
            # Role-based redirection after password change
            if request.user.role == 'admin':
                return redirect('admin_dashboard')  # Redirect to admin dashboard
            elif request.user.role == 'teacher':
                return redirect('teacher_dashboard')  # Redirect to teacher dashboard
            elif request.user.role == 'student':
                return redirect('student_dashboard')  # Redirect to student dashboard
            else:
                return redirect('home')  # Fallback redirection if no valid role
            
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)
    
    return render(request, 'authentication/change_password.html', {'form': form})

def reset_password_view(request, token):
    # Retrieve the reset request based on the token
    reset_request = PasswordResetRequest.objects.filter(token=token).first()

    if not reset_request or not reset_request.is_valid():
        messages.error(request, 'The reset link is invalid or has expired.')
        return redirect('forgot_password')
    user = reset_request.user
    if request.method == 'POST':
        form = SetPasswordForm(user,request.POST)
        if form.is_valid():
            form.save()
           
            messages.success(request, 'Your password has been updated successfully.')
            reset_request.delete()
            
            # Role-based redirection
            
            return redirect('login')  # Fallback redirection
            
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)
    
    return render(request, 'authentication/reset_password.html', {'form': form})



def logout_view(request):
    logout(request)
    messages.success(request,'you have been logged out')
    return redirect('login')

def dashboard(request):
    return HttpResponse('dashboard')