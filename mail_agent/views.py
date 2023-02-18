# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils import timezone

from models import Subscriber
from .tasks import send_email_task


def index(request):
    context = {
    }
    return render(request, 'index.html', context)


def create_mailing_list(request):
    if request.method == "POST":
        data = request.POST
        datetime_mailing_time = datetime.strptime(str((data.get("mailing-time"))), "%Y-%m-%dT%H:%M")
        if datetime_mailing_time < datetime.now():
            return JsonResponse(
                data={'error': "Время рассылки должно быть больше текущего."},
                status=400
            )
        #TODO обработка рассылки
        return JsonResponse(data={}, status=201)
    else:
        return JsonResponse(
            data={},
            status=404
        )
    # email_from = 'dyadkayar59@yandex.ru'
    # mails = []
    # subscribers = Subscriber.objects.all()
    # for subscriber in subscribers:
    #     mails.append((
    #         'subject',
    #         'message',
    #         email_from,
    #         [subscriber.email, ],
    #     ))
    # send_email_task.delay(tuple(mails))
    return HttpResponse('success')
