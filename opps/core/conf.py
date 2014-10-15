# -*- coding: utf-8 -*-
from django.conf import settings
from appconf import AppConf


class HaystackConf(AppConf):
    CONNECTIONS = {}

    class Meta:
        prefix = 'haystack'


class OppsConf(AppConf):

    CONTAINER_TYPES = ()

    class Meta:
        prefix = 'opps'
