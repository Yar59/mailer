# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

import pytz
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags

from models import Subscriber
from .tasks import send_email_task


def index(request):
    context = {
    }
    return render(request, 'index.html', context)


def create_mailing_list(request):
    if request.method == 'POST':
        data = request.POST

        mailing_time = datetime.strptime(str((data.get('mailing-time'))), '%Y-%m-%dT%H:%M')
        local_mailing_time = pytz.timezone('UTC').localize(mailing_time, is_dst=None)
        auth_user = data.get('auth_user')
        auth_password = data.get('auth_password')
        subject = data.get('subject')
        if timezone.localtime(local_mailing_time) < timezone.localtime(timezone.now()):
            return JsonResponse(
                data={
                    'status': 400,
                    'error': 'Время рассылки должно быть больше текущего.'
                },
                status=400
            )
        email_from = auth_user

        subscribers = Subscriber.objects.all()
        for subscriber in subscribers:
            tracking_link_template = 'http://www.google-analytics.com/' \
                                     'collect?v=1&tid={tracking_id}&t=event&cid={recipient_id}&ec=kinetic&ea=open'
            tracking_link = tracking_link_template.format(tracking_id=settings.TRACKING_ID, recipient_id=subscriber.id)
            html_message = render_to_string(
                '../templates/message_template.html',
                {
                    'name': subscriber.name,
                    'birthday': subscriber.birthday,
                    'tracking_link': tracking_link,
                }
            )
            plain_message = strip_tags(html_message)
            send_email_task.apply_async(
                (
                    subject,
                    plain_message,
                    email_from,
                    [subscriber.email, ],
                    html_message,
                    auth_user,
                    auth_password,
                ),
                eta=local_mailing_time
            )

        return JsonResponse(
            data={
                'status': 201
            },
            status=201
        )
    else:
        return JsonResponse(
            data={
                'status': 404,
                'error': 'Только POST запросы'
            },
            status=404
        )
