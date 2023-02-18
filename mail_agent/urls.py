from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_mailing_list/$', views.create_mailing_list, name='mailing'),
]
