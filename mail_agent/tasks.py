from celery import shared_task
from django.core.mail import send_mass_mail


@shared_task
def send_email_task(mails):
    send_mass_mail(mails)
