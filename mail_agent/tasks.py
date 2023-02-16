from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email_task():
    send_mail(
        'Celery task worked!',
        'This is proof of work!',
        'DyadkaYar59@yandex.ru',
        ['DyadkaYar59@yandex.ru'],
    )
