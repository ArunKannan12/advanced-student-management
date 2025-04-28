from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.signing import Signer
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

def send_verification_email(self):
        signer = Signer()
        uid = urlsafe_base64_encode(force_bytes(self.pk))  # Encode user ID
        token = signer.sign(self.email)  # Create a token for this user (sign their email)

        verification_link = f"http://{get_current_site(None).domain}{reverse('email_verification', kwargs={'uidb64': uid, 'token': token})}"

        subject = 'Verify your email address'
        message = render_to_string('authentication/verify_email.html', {
            'user': self,
            'verification_link': verification_link,
        })

        send_mail(
            subject,
            message,
            'arunachu962@gmail.com',  # Your email here
            [self.email],
            fail_silently=False,
        )