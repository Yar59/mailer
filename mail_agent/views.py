# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

import pytz
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
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
    if request.method == "POST":
        data = request.POST
        mailing_time = datetime.strptime(str((data.get("mailing-time"))), "%Y-%m-%dT%H:%M")
        local_mailing_time = pytz.timezone("UTC").localize(mailing_time, is_dst=None)
        if timezone.localtime(local_mailing_time) < timezone.localtime(timezone.now()):
            return JsonResponse(
                data={
                    'status': 400,
                    'error': 'Время рассылки должно быть больше текущего.'
                },
                status=400
            )
        email_from = 'dyadkayar59@yandex.ru'
        subscribers = Subscriber.objects.all()
        for subscriber in subscribers:
            html_message = render_to_string('../templates/message_template.html', {'context': 'values'})
            plain_message = strip_tags(html_message)
            send_email_task.apply_async(
                (
                'subject',
                plain_message,
                email_from,
                [subscriber.email, ],
                html_message,
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
