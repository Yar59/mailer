import smtplib

from celery import shared_task
from django.core.mail import send_mail


@shared_task(bind=True, default_retry_delay=10 * 60)
def send_email_task(self, subject, message, email_from, recipient_list, html_message=None):
    try:
        send_mail(subject, message, email_from, recipient_list, html_message=html_message)
    except smtplib.SMTPException as ex:
        self.retry(exc=ex, countdown=5)
