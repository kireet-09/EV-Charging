import smtplib
import ssl
from django.core.mail import send_mail
from django.conf import settings

def send_reservation_email(user_email, subject, message):
    context = ssl._create_unverified_context()  # ❌ Skips SSL verification (temporary fix)
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
        connection=None if settings.EMAIL_USE_TLS else context,
    )
